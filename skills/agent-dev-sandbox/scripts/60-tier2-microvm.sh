#!/usr/bin/env bash
# ============================================================================
# 60-tier2-microvm.sh — KVM micro-VM tier (container-in-VM, hostile workloads)
# ============================================================================
# Threat model Tier 2: full kernel boundary between the workload and the host.
# A golden Debian 13 VM is built ONCE (cloud-init: podman + nftables egress
# enforcement + the Tier-1 agent image loaded). Each project then gets an
# instant copy-on-write overlay that runs THE SAME agent-dev-sandbox container
# image inside the VM — one source of truth, two isolation tiers.
#
# VM egress is enforced by nftables INSIDE the VM: only the host allowlist
# proxy (10.0.2.2:3128 via QEMU user-net) and slirp DNS (10.0.2.3) may leave.
# Workspaces live on the VM disk (never bind-mounted from the host) — export
# artifacts out via scp BEFORE destroy.
#
# Usage:
#   scripts/60-tier2-microvm.sh base                # one-time golden build
#   scripts/60-tier2-microvm.sh create <name>       # instant overlay VM
#   scripts/60-tier2-microvm.sh ssh <name>          # shell into the VM
#   scripts/60-tier2-microvm.sh start|stop <name>
#   scripts/60-tier2-microvm.sh list
#   scripts/60-tier2-microvm.sh destroy <name>      # DELETES VM DISK (code too!)
# ============================================================================
set -euo pipefail

VM_DIR="${HOME}/.local/share/agent-sandbox/microvm"
GOLDEN="${VM_DIR}/golden-agent.qcow2"
BASE_DIR="${VM_DIR}/base"
KEY="${VM_DIR}/id_ed25519"
IMAGE="agent-dev-sandbox:1"
GOLDEN_PORT=2222
VM_MEM_MB=6144
VM_CPUS=4

ARCH="$(uname -m)"
case "${ARCH}" in
    x86_64) QEMU_BIN=qemu-system-x86_64; CLOUD_ARCH=amd64 ;;
    aarch64) QEMU_BIN=qemu-system-aarch64; CLOUD_ARCH=arm64 ;;
    *) echo "unsupported arch ${ARCH}" >&2; exit 1 ;;
esac
CLOUD_URL="https://cloud.debian.org/images/cloud/trixie/latest/debian-13-genericcloud-${CLOUD_ARCH}.qcow2"

RED='\033[0;31m'; GREEN='\033[0;32m'; NC='\033[0m'
ok()   { echo -e "  ${GREEN}✓${NC} $1"; }
info() { echo "  → $1"; }
die()  { echo -e "  ${RED}✗ $1${NC}" >&2; exit 1; }

require_kvm() {
    [ -e /dev/kvm ] || die "/dev/kvm missing — install qemu-system-x86 (bootstrap --tier2) and ensure CPU virtualization is enabled"
    [ -w /dev/kvm ] || die "/dev/kvm not writable — add yourself to the kvm group (bootstrap --tier2) and RE-LOGIN"
    command -v "${QEMU_BIN}" >/dev/null || die "${QEMU_BIN} not installed — run scripts/10-host-bootstrap.sh --tier2"
    command -v cloud-localds >/dev/null || die "cloud-image-utils not installed — run scripts/10-host-bootstrap.sh --tier2"
}

vm_ssh() { # vm_ssh <port> [cmd...]
    local port="$1"; shift
    ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
        -o ConnectTimeout=10 -o LogLevel=ERROR -i "${KEY}" -p "${port}" dev@127.0.0.1 "$@"
}

wait_ssh() { # wait_ssh <port> <label>
    local port="$1" label="$2"
    info "waiting for SSH on 127.0.0.1:${port} (${label}; first boot runs cloud-init, be patient)…"
    for _ in $(seq 1 90); do
        if vm_ssh "${port}" true 2>/dev/null; then ok "SSH up (${label})"; return 0; fi
        sleep 10
    done
    die "SSH never came up for ${label} — console log: ${VM_DIR}/logs/${label}.console.log (cloud-init failure? see references/troubleshooting.md §8)"
}

boot_vm() { # boot_vm <name> <disk> <port> [seed.iso]
    local name="$1" disk="$2" port="$3" seed="${4:-}"
    mkdir -p "${VM_DIR}/logs" "${VM_DIR}/pids"
    local seed_args=()
    [ -n "${seed}" ] && seed_args=(-drive "file=${seed},if=virtio,media=cdrom,readonly=on")
    # shellcheck disable=SC2086
    "${QEMU_BIN}" \
        -name "agent-sandbox-${name}" \
        -machine accel=kvm:tcg -cpu host \
        -smp "${VM_CPUS}" -m "${VM_MEM_MB}" \
        -drive "file=${disk},if=virtio,format=qcow2" \
        "${seed_args[@]}" \
        -nic "user,model=virtio-net,hostfwd=tcp:127.0.0.1:${port}-:22" \
        -display none -daemonize \
        -serial "file:${VM_DIR}/logs/${name}.console.log" \
        -pidfile "${VM_DIR}/pids/${name}.pid"
}

port_file()  { echo "${VM_DIR}/ports.${1}"; }
disk_file()  { echo "${VM_DIR}/vm-${1}.qcow2"; }

alloc_port() {
    local p=2230
    while grep -qs "^${p}$" "${VM_DIR}"/ports.* 2>/dev/null; do
        p=$((p+1))
    done
    echo "${p}"
}

vm_running() { # vm_running <name>
    [ -f "${VM_DIR}/pids/${1}.pid" ] && kill -0 "$(cat "${VM_DIR}/pids/${1}.pid")" 2>/dev/null
}

ensure_key() {
    if [ ! -f "${KEY}" ]; then
        mkdir -p "${VM_DIR}"
        ssh-keygen -q -t ed25519 -N "" -C "agent-sandbox-microvm" -f "${KEY}"
        ok "generated VM access key ${KEY}"
    fi
}

# ----------------------------------------------------------------------------
cmd_base() {
    require_kvm
    ensure_key
    mkdir -p "${BASE_DIR}"

    # 1. Official Debian 13 cloud image + SHA512 verification
    local img="${BASE_DIR}/debian-13-genericcloud-${CLOUD_ARCH}.qcow2"
    if [ ! -f "${img}" ]; then
        info "downloading ${CLOUD_URL} (~350 MB)…"
        curl -fL --retry 3 -o "${img}" "${CLOUD_URL}"
        curl -fsL -o "${BASE_DIR}/SHA512SUMS" "https://cloud.debian.org/images/cloud/trixie/latest/SHA512SUMS"
        ( cd "${BASE_DIR}" && grep " $(basename "${img}")$" SHA512SUMS | sha512sum -c - ) \
            || die "SHA512 mismatch on the cloud image — delete ${img} and retry"
        ok "cloud image downloaded + SHA512 verified"
    fi

    # 2. Golden overlay + cloud-init seed (NoCloud)
    local work="${VM_DIR}/golden-work"; rm -rf "${work}"; mkdir -p "${work}"
    qemu-img create -f qcow2 -F qcow2 -b "${img}" "${work}/golden.qcow2" 30G >/dev/null
    ok "golden overlay created (30G virtual)"

    cat > "${work}/user-data" <<EOF
#cloud-config
hostname: golden-agent
users:
  - name: dev
    shell: /bin/bash
    groups: [sudo]
    sudo: ALL=(ALL) NOPASSWD:ALL
    lock_passwd: true
    ssh_authorized_keys:
      - $(cat "${KEY}.pub")
package_update: true
packages: [podman, crun, uidmap, passt, slirp4netns, nftables, curl, ca-certificates]
write_files:
  - path: /etc/apt/apt.conf.d/95-agent-sandbox-proxy
    content: |
      Acquire::http::Proxy "http://10.0.2.2:3128";
      Acquire::https::Proxy "http://10.0.2.2:3128";
  - path: /etc/profile.d/agent-sandbox-proxy.sh
    content: |
      export http_proxy=http://10.0.2.2:3128
      export https_proxy=http://10.0.2.2:3128
      export HTTP_PROXY=http://10.0.2.2:3128
      export HTTPS_PROXY=http://10.0.2.2:3128
      export no_proxy=localhost,127.0.0.1,::1
      export NO_PROXY=localhost,127.0.0.1,::1
  - path: /etc/nftables.conf
    content: |
      #!/usr/sbin/nft -f
      # VM egress enforcement: only the host allowlist proxy and slirp DNS leave.
      flush ruleset
      table inet filter {
        chain input {
          type filter hook input priority 0; policy drop;
          ct state established,related accept
          iif "lo" accept
          tcp dport 22 accept
          ip protocol icmp accept
        }
        chain forward {
          type filter hook forward priority 0; policy drop;
        }
        chain output {
          type filter hook output priority 0; policy drop;
          oif "lo" accept
          ct state established,related accept
          ip daddr 10.0.2.2 tcp dport 3128 accept
          ip daddr 10.0.2.3 udp dport 53 accept
          ip daddr 10.0.2.3 tcp dport 53 accept
          ip protocol icmp accept
        }
      }
runcmd:
  - usermod --add-subuid 100000-165535 dev
  - usermod --add-subgid 100000-165535 dev
  - sysctl -w net.ipv4.ping_group_range=0 2000000
  - loginctl enable-linger dev || true
  - systemctl enable nftables
  - systemctl restart nftables
EOF
    printf 'instance-id: golden-agent-001\nlocal-hostname: golden-agent\n' > "${work}/meta-data"
    cloud-localds "${work}/seed.iso" "${work}/user-data" "${work}/meta-data"
    ok "cloud-init seed written (apt via host proxy; nftables default-deny egress)"

    # 3. Boot golden, wait for provisioning to finish
    boot_vm golden "${work}/golden.qcow2" "${GOLDEN_PORT}" "${work}/seed.iso"
    wait_ssh "${GOLDEN_PORT}" golden
    info "waiting for cloud-init to finish (installs podman via proxy; 5-15 min)…"
    vm_ssh "${GOLDEN_PORT}" "sudo cloud-init status --wait" || {
        vm_ssh "${GOLDEN_PORT}" "sudo cloud-init status --long" || true
        die "cloud-init did not finish cleanly — console: ${VM_DIR}/logs/golden.console.log"
    }
    ok "cloud-init provisioning done"

    # 4. Transfer + load the SAME Tier-1 image into the VM
    info "exporting ${IMAGE} and transferring into the VM (1-3 GB; a few minutes)…"
    local tarball="${work}/agent-image.tar.gz"
    podman save "${IMAGE}" | gzip > "${tarball}"
    scp -q -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i "${KEY}" \
        -P "${GOLDEN_PORT}" "${tarball}" dev@127.0.0.1:/tmp/agent-image.tar.gz
    rm -f "${tarball}"
    vm_ssh "${GOLDEN_PORT}" 'gunzip -c /tmp/agent-image.tar.gz | podman load && rm /tmp/agent-image.tar.gz && podman image ls'
    ok "agent image loaded inside golden VM"

    # 5. Shut down, freeze as golden
    vm_ssh "${GOLDEN_PORT}" "sudo poweroff" || true
    for _ in $(seq 1 30); do kill -0 "$(cat "${VM_DIR}/pids/golden.pid" 2>/dev/null)" 2>/dev/null || break; sleep 2; done
    mv "${work}/golden.qcow2" "${GOLDEN}"
    rm -rf "${work}" "${VM_DIR}/pids/golden.pid"
    ok "golden image frozen at ${GOLDEN}"
    echo "  Next: scripts/60-tier2-microvm.sh create <name>"
}

# ----------------------------------------------------------------------------
cmd_create() {
    local name="${1:?usage: create <name>}"
    [[ "${name}" =~ ^[a-z][a-z0-9-]{0,38}$ ]] || die "invalid VM name '${name}'"
    [ -f "${GOLDEN}" ] || die "golden image missing — run: $0 base"
    require_kvm
    if vm_running "${name}"; then die "VM '${name}' is already running"; fi
    [ -f "$(disk_file "${name}")" ] && die "VM disk for '${name}' exists (destroy it first or pick a new name)"

    local port; port="$(alloc_port)"
    echo "${port}" > "$(port_file "${name}")"

    local disk; disk="$(disk_file "${name}")"
    qemu-img create -f qcow2 -F qcow2 -b "${GOLDEN}" "${disk}" 40G >/dev/null
    ok "overlay disk ${disk} (40G virtual, copy-on-write — instant)"

    boot_vm "${name}" "${disk}" "${port}"
    wait_ssh "${port}" "${name}"
    vm_ssh "${port}" "sudo hostnamectl set-hostname ${name}" >/dev/null

    # Workspace + secrets template INSIDE the VM (never touches the host fs)
    vm_ssh "${port}" "mkdir -p ~/workspaces/${name} ~/.config/agent-sandbox" 
    vm_ssh "${port}" "cat > ~/.config/agent-sandbox/${name}.env <<'ENVEOF'
# Secrets for VM workspace '${name}' — edit, then recreate the container below.
#ANTHROPIC_API_KEY=
#OPENAI_API_KEY=
ENVEOF
chmod 600 ~/.config/agent-sandbox/${name}.env"

    # Same hardening contract as Tier 1, inside the VM. Egress is enforced by
    # the VM's nftables (default-deny except host proxy), so the container can
    # use the default rootless network here.
    vm_ssh "${port}" "podman run -d \
        --name agent-${name} \
        --hostname ${name} \
        --userns=keep-id:uid=1000,gid=1000 \
        --cap-drop=ALL \
        --security-opt no-new-privileges \
        --pids-limit 1024 --memory 4g --cpus 2 \
        -v ~/workspaces/${name}:/workspace:Z \
        -v agent-home-${name}:/home/dev:Z \
        -e http_proxy=http://10.0.2.2:3128 \
        -e https_proxy=http://10.0.2.2:3128 \
        -e HTTP_PROXY=http://10.0.2.2:3128 \
        -e HTTPS_PROXY=http://10.0.2.2:3128 \
        -e no_proxy=localhost,127.0.0.1,::1 -e NO_PROXY=localhost,127.0.0.1,::1 \
        -e PLAYWRIGHT_BROWSERS_PATH=/home/dev/.cache/ms-playwright \
        --env-file ~/.config/agent-sandbox/${name}.env \
        ${IMAGE}" >/dev/null
    vm_ssh "${port}" "podman exec agent-${name} seed-playwright-browsers"

    ok "VM '${name}' ready (ssh port ${port}, container agent-${name} inside)"
    echo
    echo "  Enter the VM:        scripts/60-tier2-microvm.sh ssh ${name}"
    echo "  Then the container:  podman exec -it agent-${name} ws-shell"
    echo "  Export artifacts OUT before destroy — the VM disk is deleted with it."
}

# ----------------------------------------------------------------------------
cmd_ssh()   { local n="${1:?usage: ssh <name>}"; local p; p="$(cat "$(port_file "${n}")")"; vm_ssh "${p}"; }

cmd_stop() {
    local n="${1:?usage: stop <name>}"
    vm_running "${n}" || { ok "'${n}' not running"; exit 0; }
    local p; p="$(cat "$(port_file "${n}")")"
    vm_ssh "${p}" "sudo poweroff" 2>/dev/null || kill "$(cat "${VM_DIR}/pids/${n}.pid")" 2>/dev/null || true
    for _ in $(seq 1 30); do vm_running "${n}" || break; sleep 2; done
    rm -f "${VM_DIR}/pids/${n}.pid"
    ok "'${n}' stopped (disk + workspace preserved)"
}

cmd_start() {
    local n="${1:?usage: start <name>}"
    [ -f "$(disk_file "${n}")" ] || die "no disk for '${n}'"
    vm_running "${n}" && die "'${n}' already running"
    require_kvm
    local p; p="$(cat "$(port_file "${n}")")"
    boot_vm "${n}" "$(disk_file "${n}")" "${p}"
    wait_ssh "${p}" "${n}"
    ok "'${n}' started"
}

cmd_list() {
    printf "  %-18s %-10s %-6s %s\n" "VM" "STATE" "PORT" "DISK"
    local n
    for f in "${VM_DIR}"/vm-*.qcow2; do
        [ -e "$f" ] || break
        n="$(basename "$f" .qcow2)"; n="${n#vm-}"
        local state="stopped"; vm_running "${n}" && state="running"
        local port="-"; [ -f "$(port_file "${n}")" ] && port="$(cat "$(port_file "${n}")")"
        printf "  %-18s %-10s %-6s %s\n" "${n}" "${state}" "${port}" "$f"
    done
}

cmd_destroy() {
    local n="${1:?usage: destroy <name>}"
    cmd_stop "${n}" 2>/dev/null || true
    echo -e "  ${RED}WARNING: this deletes the VM disk INCLUDING all code inside the VM.${NC}"
    echo -e "  Export anything you need first:  scp -i ${KEY} -P $(cat "$(port_file "${n}")" 2>/dev/null || echo PORT) -r dev@127.0.0.1:~/workspaces/${n} ."
    read -r -p "  Type the VM name to confirm deletion: " confirm
    [ "${confirm}" = "${n}" ] || die "aborted"
    rm -f "$(disk_file "${n}")" "$(port_file "${n}")" "${VM_DIR}/pids/${n}.pid"
    ok "VM '${n}' destroyed"
}

main() {
    [ $# -ge 1 ] || { sed -n '2,20p' "${BASH_SOURCE[0]}"; exit 2; }
    local cmd="$1"; shift
    case "${cmd}" in
        base)    cmd_base ;;
        create)  cmd_create "${1:?usage: create <name>}" ;;
        ssh)     cmd_ssh "$@" ;;
        start)   cmd_start "${1:?usage: start <name>}" ;;
        stop)    cmd_stop "${1:?usage: stop <name>}" ;;
        list)    cmd_list ;;
        destroy) cmd_destroy "${1:?usage: destroy <name>}" ;;
        *) sed -n '2,20p' "${BASH_SOURCE[0]}"; exit 2 ;;
    esac
}
main "$@"
