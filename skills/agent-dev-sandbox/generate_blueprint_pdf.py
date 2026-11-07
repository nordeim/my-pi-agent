#!/usr/bin/env python3
# generate_blueprint_pdf.py — body PDF for the Agent Dev Sandbox blueprint.
# Report route (ReportLab). Cover is rendered separately via html2poster.js
# and merged as page 0 (see build steps in the task notes).
#
# Style contract (briefs/report.md + typesetting/*):
#   * fonts: FreeSerif body/headings, DejaVuSans (mono) for code — allowed set only
#   * install_font_fallback() called once after registration
#   * TOC: TocDocTemplate + multiBuild + bookmark keys (clickable)
#   * H1: CondPageBreak(25% page) — never forced PageBreak between sections
#   * tables: all cells Paragraph(), proportional colWidths, repeatRows=1,
#     HEADER_FILL header + TABLE_STRIPE odd rows, hAlign='CENTER'
#   * code blocks: Preformatted in a 1x1 table (CARD_BG + accent left border)
#   * figure: block-level Image() with caption, KeepTogether, fit to width
import os
import re
import sys
import hashlib

PDF_SKILL_DIR = './skills/pdf'
sys.path.insert(0, os.path.join(PDF_SKILL_DIR, 'scripts'))

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, CondPageBreak, Image, Preformatted, HRFlowable,
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily, stringWidth
from PIL import Image as PILImage

# ---------------------------------------------------------------- fonts
FONT_DIR = '/usr/share/fonts'
pdfmetrics.registerFont(TTFont('NotoSerifSC', f'{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Regular.ttf'))
pdfmetrics.registerFont(TTFont('NotoSerifSC-Bold', f'{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Bold.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif', f'{FONT_DIR}/truetype/freefont/FreeSerif.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Bold', f'{FONT_DIR}/truetype/freefont/FreeSerifBold.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Italic', f'{FONT_DIR}/truetype/freefont/FreeSerifItalic.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-BoldItalic', f'{FONT_DIR}/truetype/freefont/FreeSerifBoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', f'{FONT_DIR}/truetype/dejavu/DejaVuSansMono.ttf'))
registerFontFamily('NotoSerifSC', normal='NotoSerifSC', bold='NotoSerifSC-Bold')
registerFontFamily('FreeSerif', normal='FreeSerif', bold='FreeSerif-Bold',
                   italic='FreeSerif-Italic', boldItalic='FreeSerif-BoldItalic')
registerFontFamily('DejaVuSans', normal='DejaVuSans', bold='DejaVuSans')

from pdf import install_font_fallback  # noqa: E402  (skill scripts dir)
install_font_fallback()

# ------------------------------------------------------- palette (cascade, seed 42)
PAGE_BG       = colors.HexColor('#f4f5f5')
SECTION_BG    = colors.HexColor('#f0f1f2')
CARD_BG       = colors.HexColor('#e8eaeb')
TABLE_STRIPE  = colors.HexColor('#ebeded')
HEADER_FILL   = colors.HexColor('#32454e')
COVER_BLOCK   = colors.HexColor('#566a74')
BORDER        = colors.HexColor('#acbdc5')
ICON          = colors.HexColor('#4b86a4')
ACCENT        = colors.HexColor('#1f6c92')
ACCENT_2      = colors.HexColor('#c23a50')
TEXT_PRIMARY  = colors.HexColor('#131515')
TEXT_MUTED    = colors.HexColor('#747b7e')

# ---------------------------------------------------------------- geometry
MARGIN = 72  # symmetric 1 inch
PAGE_W, PAGE_H = A4
AVAIL_W = PAGE_W - 2 * MARGIN            # ~451 pt
AVAIL_H = PAGE_H - 2 * MARGIN            # ~698 pt
H1_COND_BREAK = AVAIL_H * 0.25

OUT = './scripts/pdf-build/blueprint-body.pdf'
DIAGRAM = './scripts/pdf-build/diagram.png'

# ---------------------------------------------------------------- styles
body = ParagraphStyle('Body', fontName='FreeSerif', fontSize=10.5, leading=17,
                      alignment=TA_JUSTIFY, textColor=TEXT_PRIMARY,
                      spaceBefore=0, spaceAfter=8)
lede = ParagraphStyle('Lede', parent=body, fontSize=10.5, leading=17,
                      textColor=TEXT_PRIMARY, spaceAfter=10)
bullet = ParagraphStyle('Bullet', parent=body, alignment=TA_LEFT,
                        leftIndent=16, bulletIndent=4, spaceAfter=5)
h1 = ParagraphStyle('H1', fontName='FreeSerif', fontSize=20, leading=25,
                    textColor=HEADER_FILL, spaceBefore=0, spaceAfter=4,
                    alignment=TA_LEFT)
h3 = ParagraphStyle('H3', fontName='FreeSerif', fontSize=11.5, leading=16,
                    textColor=TEXT_PRIMARY, spaceBefore=10, spaceAfter=4)
caption = ParagraphStyle('Caption', fontName='FreeSerif', fontSize=8.5,
                         leading=12, textColor=TEXT_MUTED, alignment=TA_CENTER,
                         spaceBefore=3, spaceAfter=6)
quote = ParagraphStyle('Quote', parent=body, fontName='FreeSerif-Italic',
                       leftIndent=24, textColor=TEXT_PRIMARY,
                       borderPadding=0, spaceBefore=6, spaceAfter=10,
                       alignment=TA_LEFT)
code_style = ParagraphStyle('Code', fontName='DejaVuSans', fontSize=8.5,
                            leading=11.6, textColor=TEXT_PRIMARY)
cell = ParagraphStyle('Cell', fontName='FreeSerif', fontSize=9, leading=12.5,
                      textColor=TEXT_PRIMARY, alignment=TA_LEFT)
cell_hdr = ParagraphStyle('CellHdr', fontName='FreeSerif', fontSize=9,
                          leading=12, textColor=colors.white, alignment=TA_LEFT)
toc_l0 = ParagraphStyle('TOC0', fontName='FreeSerif', fontSize=11, leading=20,
                        leftIndent=6, textColor=TEXT_PRIMARY)
toc_title = ParagraphStyle('TOCTitle', fontName='FreeSerif', fontSize=20,
                           leading=26, textColor=HEADER_FILL, spaceAfter=14)


def esc(t):
    # entity-escape for ReportLab paraparser (single quotes avoid any
    # tool-layer entity decoding of the literal strings below)
    t = t.replace(chr(38), chr(38) + 'amp;')
    t = t.replace(chr(60), chr(38) + 'lt;')
    t = t.replace(chr(62), chr(38) + 'gt;')
    return t


def fmt(t, code_size=9):
    """Minimal inline markdown -> ReportLab intra-paragraph markup."""
    t = esc(t)
    t = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',
               r'<link href="\2" color="#1f6c92">\1</link>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'`([^`]+)`',
               lambda m: '<font face="DejaVuSans" size="%.1f">%s</font>'
                         % (code_size, m.group(1)),
               t)
    return t


def P(text, style=body, code_size=9):
    return Paragraph(fmt(text, code_size), style)


def B(text):
    return Paragraph(fmt(text), bullet, bulletText='\u2022')


def heading(num_title):
    """H1 with TOC bookmark + accent underline, orphan-protected."""
    key = 'h_' + hashlib.md5(num_title.encode()).hexdigest()[:8]
    p = Paragraph('<a name="%s"/><b>%s</b>' % (key, esc(num_title)), h1)
    p.bookmark_name = key
    p.bookmark_level = 0
    p.bookmark_text = num_title
    p.bookmark_key = key
    rule = HRFlowable(width='100%', thickness=1.2, color=ACCENT,
                      spaceBefore=0, spaceAfter=10)
    return [CondPageBreak(H1_COND_BREAK), Spacer(1, 24),
            KeepTogether([p, rule])]


def code_block(lines):
    fs = 8.5
    longest = max((stringWidth(l, 'DejaVuSans', fs) for l in lines), default=0)
    inner = AVAIL_W - 24
    while longest > inner and fs > 7.6:
        fs -= 0.25
        longest = max(stringWidth(l, 'DejaVuSans', fs) for l in lines)
    st = ParagraphStyle('CodeS', parent=code_style, fontSize=fs,
                        leading=fs * 1.38)
    pre = Preformatted('\n'.join(lines), st)
    t = Table([[pre]], colWidths=[AVAIL_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CARD_BG),
        ('LINEBEFORE', (0, 0), (0, -1), 2.2, ACCENT),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    return [Spacer(1, 6), t, Spacer(1, 10)]


def make_table(header, rows, ratios, font=9):
    cs = ParagraphStyle('CellS', parent=cell, fontSize=font, leading=font + 3.5)
    hs = ParagraphStyle('CellHS', parent=cell_hdr, fontSize=font,
                        leading=font + 3)
    data = [[Paragraph('<b>%s</b>' % fmt(c, font), hs) for c in header]]
    for r in rows:
        data.append([Paragraph(fmt(c, font), cs) for c in r])
    widths = [r * AVAIL_W for r in ratios]
    assert abs(sum(widths) - AVAIL_W) < 1.0, 'colWidths must fill available width'
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='CENTER')
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_FILL),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        style.append(('BACKGROUND', (0, i), (-1, i),
                      TABLE_STRIPE if i % 2 else colors.white))
    t.setStyle(TableStyle(style))
    return t


def table_block(header, rows, ratios, cap, font=9):
    t = make_table(header, rows, ratios, font)
    # Table + caption travel together: an orphaned caption on the next page
    # is a layout defect (all tables here are <= 14 rows, well under the
    # 40%-page KeepTogether cap).
    return [Spacer(1, 12), KeepTogether([t, Spacer(1, 6), P(cap, caption)]),
            Spacer(1, 12)]


def callout(text):
    st = ParagraphStyle('CalloutText', parent=body, fontSize=11, leading=16.5,
                        textColor=HEADER_FILL, alignment=TA_LEFT, spaceAfter=0)
    t = Table([[Paragraph(fmt(text), st)]], colWidths=[AVAIL_W * 0.92],
              hAlign='CENTER')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), SECTION_BG),
        ('LINEBEFORE', (0, 0), (0, -1), 3, ACCENT),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
    ]))
    return [Spacer(1, 8), KeepTogether([t]), Spacer(1, 10)]


def figure(path, cap):
    pil = PILImage.open(path)
    ow, oh = pil.size
    max_w, max_h = AVAIL_W, 360
    ratio = min(max_w / ow, max_h / oh)
    img = Image(path, width=ow * ratio, height=oh * ratio)
    return [Spacer(1, 10), CondPageBreak(oh * ratio + 40),
            KeepTogether([img, P(cap, caption)]), Spacer(1, 8)]


# ---------------------------------------------------------------- doc template
class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'bookmark_name'):
            level = getattr(flowable, 'bookmark_level', 0)
            text = getattr(flowable, 'bookmark_text', '')
            key = getattr(flowable, 'bookmark_key', '')
            self.notify('TOCEntry', (level, text, self.page, key))


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont('FreeSerif', 7.5)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(MARGIN, PAGE_H - 42,
                      'Agent Dev Sandbox \u2014 Comprehensive Blueprint')
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.2)
    canvas.line(MARGIN, PAGE_H - 48, PAGE_W - MARGIN, PAGE_H - 48)
    if doc.page > 1:  # TOC page stays unnumbered
        canvas.setFont('FreeSerif', 7.5)
        canvas.setFillColor(TEXT_MUTED)
        canvas.drawString(MARGIN, 32,
                          'Debian 13 \u00b7 egress-restricted workspaces for AI coding agents')
        canvas.drawRightString(PAGE_W - MARGIN, 32, str(doc.page))
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, 44, PAGE_W - MARGIN, 44)
    canvas.restoreState()


# ---------------------------------------------------------------- content
story = []

# ---- TOC page (front matter; body sections start on the next page)
story.append(Paragraph('<b>Table of Contents</b>', toc_title))
toc = TableOfContents()
toc.levelStyles = [toc_l0]
story.append(toc)
story.append(PageBreak())

# ---- 1. Executive summary
story += heading('1. Executive summary')
story.append(P('The environment is a two-tier "container-first, VM-when-paranoid" design, with a third consumption mode of the same image for ephemeral CI runs.', lede))
story.append(P('**Tier 1 \u2014 daily driver.** One persistent, hardened, *rootless* Podman container per project. The container runs with zero Linux capabilities, `no-new-privileges`, user-namespace mapping (`keep-id`), and cgroup caps. It sits on an *internal* Podman network that has **no default route and no external DNS**. Egress exists through exactly one path: a rootless Squid gateway enforcing a single-file domain allowlist. Everything an agent needs \u2014 Python 3.13, Node 24, Bun, pnpm, uv, git, ripgrep, SQLite, Chromium, Playwright (Node + Python), agent-browser, and the three agent CLIs \u2014 is baked into one reproducible image.'))
story.append(P('**Tier 2 \u2014 hostile workloads.** A KVM micro-VM per engagement, booted from an official Debian 13 cloud image, provisioned by cloud-init, with egress enforced on BOTH sides: host-side QEMU user-net restrict=on (only an ssh hostfwd and a proxy guestfwd exist) plus nftables *inside* the VM (default-deny, proxy only \u2014 no DNS rule). Inside the VM runs the **same** container image via rootless Podman \u2014 one source of truth, two boundaries.'))
story.append(P('**CI mode \u2014 same image, throwaway.** A third consumption mode (\u00a712): single-shot ephemeral containers for PR checks and batch jobs, with a per-run isolation self-audit, artifact export, walltime caps, shared package caches, and a reaper for orphans. One image, three modes \u2014 interactive workspace, ephemeral CI run, container-in-VM.'))
story.append(P('Secrets never enter images: per-workspace env files (mode 0600) are injected at container start. The verification suite (`scripts/50-verify.sh`) proves both function and isolation \u2014 including *negative* tests that must fail (direct egress, external DNS) \u2014 and its output is the evidence standard for "done".'))
story.append(P('All external facts in this document were verified against live sources on **2026-11-05** (npm registry, Docker Hub, cloud.debian.org, podman documentation, the budget-wiser repository); audit remediations were applied and re-verified on **2026-11-06** (see `references/audit-remediation.md` \u2014 the external audit\u2019s 22 findings, their validation, and the fixes), a second-pass validation on **2026-11-07** closed four residual defects (S-1\u2013S-4), and a third-pass review the same day validated and remediated its eight follow-up findings (R-1\u2013R-8). Version pins appear as `ARG`s in `files/Containerfile`; bump them deliberately.'))

# ---- 2. Goals, non-goals, threat model
story += heading('2. Goals, non-goals, threat model')
story.append(P('**Goals**', h3))
story.append(B('Develop and test codebases you would otherwise run yourself (representative workload: [nordeim/budget-wiser](https://github.com/nordeim/budget-wiser) \u2014 Next.js 16, React 19, TypeScript strict, Prisma 6 + SQLite, Vitest, Playwright E2E, Bun \u2265 1.3 / Node \u2265 24). Untrusted code belongs in Tier 2.'))
story.append(B('Contain the blast radius of agent-executed code: no host filesystem access beyond the project dir, no capabilities, capped resources, no arbitrary network egress.'))
story.append(B('Self-contained: no dependency on host-installed dev tooling; workspaces are disposable and reproducible.'))
story.append(B('Agent-usable: CLIs, browsers, and shell ergonomics work out of the box; a single scripted lifecycle for everything.'))
story.append(B('Auditable: one file is the egress policy; every guarantee has a check.'))
story.append(P('**Non-goals** (see `references/hardening.md` \u00a76): multi-tenant fleets; TLS interception of proxied traffic; defending against kernel zero-days from Tier-1 workloads (that is Tier 2\u2019s job); hiding allowed-channel data flows (e.g., `git push` to an allowed host).'))
story.append(P('**Threat model \u2014 two tiers**', h3))
story += table_block(
    ['', 'Tier 1 (container)', 'Tier 2 (micro-VM)'],
    [
        ['Use when', 'Building/fixing known codebases (your own, curated OSS \u2014 code you would run yourself)', 'Auditing/running unknown repos, untrusted builds, anything that executes arbitrary scripts'],
        ['Boundary', 'Kernel namespaces + seccomp + cap-drop (shared kernel)', 'Full hardware-virtualized kernel boundary'],
        ['Egress', 'Internal network \u2192 allowlist proxy (structural: no route exists otherwise)', 'Host-side QEMU restrict=on (proxy-only guestfwd) \u2192 VM nftables default-deny \u2192 host allowlist proxy \u2014 enforced on BOTH sides'],
        ['Residual risk', 'Kernel exploit escaping to host user (mitigated: rootless, non-root, no caps); workload-user escape lands on your own account (keep-id) \u2014 hence the tier discipline', 'VM escape (hypervisor-class, rare); supply chain of allowlisted domains'],
        ['Cost', '~2 GB RAM/workspace, seconds to start', '~6 GB RAM/VM, one-time 15-30 min golden build, ~30 s per overlay boot'],
    ],
    [0.14, 0.43, 0.43],
    'Table 1 \u2014 Threat model by tier.', font=8.5)

# ---- 3. Reference implementation survey
story += heading('3. Reference implementation survey')
story.append(P('The producing environment for this blueprint is itself a Debian 13 sandbox running an AI coding agent (this document was generated inside it), which doubles as a working reference of a *functional* agent toolchain:'))
story += table_block(
    ['Component', 'Reference version', 'Note'],
    [
        ['OS', 'Debian 13.4 "trixie"', 'Same distro as the target host'],
        ['Python', '3.13.5 (`python3.13`)', 'trixie ships 3.13 as `python3`'],
        ['`python3.13-venv`', 'required, separate package', '**Gotcha verified here:** `python3 -m venv` fails without it'],
        ['Node.js', '24.22.2 (NodeSource `node_24.x`)', 'Same repo used by the Containerfile'],
        ['npm / pnpm', '11.19.1 / 12.16.1', 'pnpm via corepack'],
        ['Bun', '1.3.14', "budget-wiser\u2019s primary runtime"],
        ['uv', '0.13.7', 'standalone installer, pinned in image'],
        ['git', '2.47.3', ''],
        ['Playwright (Node)', '1.57.0 \u2192 image pins 1.64.1', '1.64.x matches budget-wiser'],
        ['Playwright browsers', 'chromium-1200 + headless shell + ffmpeg (613 MB in `~/.cache/ms-playwright`)', 'Motivates the shared `/opt` bake + per-home seeding'],
        ['agent-browser', '0.41.1 (npm latest 0.41.2)', '**Verified:** downloads its *own* Chrome 157 to `~/.agent-browser/browsers/` \u2014 independent of Playwright\u2019s Chromium'],
        ['trixie packages (verified via `apt-cache policy`)', 'podman 5.4.2, passt, slirp4netns 1.2.1, crun 1.21, squid 6.13, qemu 10.0.13, virtinst 5.0, cloud-image-utils 0.33, chromium 156, uidmap', 'All in main trixie repos'],
        ['Debian cloud image', '`debian-13-genericcloud-amd64.qcow2` at `cloud.debian.org/images/cloud/trixie/latest/` (+ `SHA512SUMS`)', 'Tier-2 base, checksum-verified by script'],
        ['Agent CLIs (npm, live)', 'claude-code 2.1.318 \u00b7 @openai/codex 0.166.0 \u00b7 opencode-ai 1.19.5', 'All installable via `npm -g`; native installers also exist'],
    ],
    [0.22, 0.40, 0.38],
    'Table 2 \u2014 Reference implementation survey (all versions verified 2026-11-05).', font=8.5)

# ---- 4. Architecture decisions
story += heading('4. Architecture decisions (ADR summary)')
adrs = [
    ('D1 \u2014 Podman (rootless) over Docker CE.',
     'Rootless Podman never needs a root daemon: container *root* maps to an unprivileged subordinate uid, so a container-root escape lands with no host permissions. Be precise about the other case: with `keep-id:uid=1000` the *workload* user `dev` IS the host user \u2014 an escape *as the workload* lands on your own account. Tier 1 is therefore for code you would run yourself; untrusted code belongs in Tier 2. No setuid daemon; lifecycle via systemd user units (Quadlet). Docker\u2019s daemon requires root or rootlesskit wrappers and adds a `docker.sock` foot-gun this design refuses to have. Podman 5.4 in trixie supports everything needed (defined networks, `--internal`, `keep-id:uid=`, Quadlet, multi-`Network=`).'),
    ('D2 \u2014 Egress enforcement by *network topology*, not by env-var etiquette.',
     '`podman network create --internal` (verified against `podman-network-create(1)`) gives attached containers **no default route**, disables IP forwarding on the bridge, and makes aardvark-dns answer **only container names** (everything else NXDOMAIN). Workspaces cannot bypass the proxy even if they ignore proxy env vars \u2014 there is no route to bypass with. The gateway is dual-homed: `agent-egress` (normal NAT network) + `agent-internal` (the isolated side). An env-var-only proxy would be trivially bypassable; host-firewall approaches cannot distinguish rootless container traffic from the user\u2019s own processes. Topology wins.'),
    ('D3 \u2014 Squid allowlist over deny-all+mirrors.',
     'Considered Verdaccio/devpi/apt-cacher mirrors (offline-first). Rejected as default: three caches to run and keep healthy, and agents legitimately need *docs and APIs*, not just packages. The allowlist proxy gives one policy file, full logging, and a 10-second change procedure (`30-gateway.sh allow`). Trade-off stated openly: an allowlisted domain is a standing grant \u2014 treat the file as production config.'),
    ('D4 \u2014 Browsers baked once, seeded per-workspace.',
     'Two browser ecosystems must coexist (\u00a73): Playwright\u2019s Chromium (per-version revisions) and agent-browser\u2019s own Chrome. Both are baked into `/opt` (image layers, ~2 GB unpacked, shared by every workspace) and *symlinked* into each workspace\u2019s writable home by an idempotent seeder. Projects pinning other Playwright versions download their revision through the proxy into their home volume \u2014 self-healing, no copy overhead for the common case.'),
    ('D5 \u2014 `--userns=keep-id:uid=1000,gid=1000`.',
     'Rootless containers otherwise remap the host user to container-root, making bind-mounted project dirs unowned by the workspace user. `keep-id:uid=1000` pins host user \u2194 container `dev` (uid 1000) regardless of the host uid, so `~/agent-workspaces/<name>` is transparently shared (IDE-editable on the host) and writable in-container. This also eliminates git\u2019s "dubious ownership" class of failures.'),
    ('D6 \u2014 One image, two tiers (container-in-VM).',
     'The Tier-2 VM runs rootless Podman *inside* it and loads the *same* `agent-dev-sandbox:1` image (transferred during the one-time golden build). Toolchain drift between tiers becomes impossible; only the enforcement point differs (VM nftables instead of network topology). The CI profile extends the same principle: `files/ci-setup.sh` is bind-mounted per run, so the image itself stays byte-identical across all three consumption modes.'),
    ('D7 \u2014 No sudo inside workspaces.',
     'A missing system package is an image bug: rebuild (minutes, cached). Granting sudo would re-open privilege escalation that cap-drop and no-new-privileges just closed. Language-level installs (npm/pip/uv) are unaffected.'),
    ('D8 \u2014 Version-pinned ARGs, digest-pinned base.',
     'Every tool in the image is pinned to a version verified on 2026-11-05 (bun via a pinned installer tag); the base image is digest-pinned and the NodeSource repo key is fingerprint-verified in-build. Honest scope: top-level versions, the base digest, bun and the NodeSource key are pinned \u2014 the uv/bun installer scripts and transitive npm dependencies are fetched over TLS from trusted endpoints at build time and are not checksum-verified; browser revisions are resolved at build. Refresh = bump ARG + rebuild + re-verify; never `@latest` in the image.'),
]
for title, text in adrs:
    story.append(P('**%s** %s' % (title, text)))
story.append(P('**Alternatives considered and rejected:** gVisor/Kata (not in Debian repos; adds a kernel-interposition layer with its own trust base \u2014 reasonable future option, documented in hardening \u00a74); Firecracker/Cloud Hypervisor (excellent for fleets; QEMU+KVM is packaged, scriptable and sufficient for single-user hosts \u2014 `boot_vm()` is the only function that would change); full Docker-in-Docker (defeats isolation); remote dev containers (network dependency, opposite of self-contained).'))

# ---- 5. System design
story += heading('5. System design')
story += figure(DIAGRAM, 'Figure 1 \u2014 System design: one host, two enforcement tiers, three consumption modes of one image.')
story.append(P('**Life of an egress request (the guarantee, step by step).** A workspace process runs `bun install`. Bun reads `https_proxy` (injected as container env) and sends `CONNECT registry.npmjs.org:443` to `agent-gateway:3128` \u2014 the name resolves via aardvark-dns to the gateway\u2019s `agent-internal` interface, because that is the only resolver reachable. Squid matches the CONNECT target against the allowlist file (bind-mounted read-only from the skill bundle): allowed \u2192 Squid itself resolves DNS and proxies the TLS tunnel (payload never decrypted); denied \u2192 HTTP 403 plus one access-log line. If the process ignores proxy variables entirely and attempts a direct socket connection, the packet is dropped at the network layer: `agent-internal` has no default route and forwarding is disabled on the bridge. If it tries to smuggle a hostname past policy, there is no external DNS to resolve it with \u2014 aardvark answers container names only, everything else NXDOMAIN.'))
story += callout('Four independent mechanisms, one policy file: no route, NXDOMAIN, proxy 403, and full per-request logging.')
story.append(P('**Workspace model (per-project, persistent).** A workspace = container + bind-mounted code dir + named home volume + env file. Stopping preserves everything; `restart` re-creates the container (re-reading the env file \u2014 key rotation without volume surgery); `snapshot` commits the container fs (env-file keys blanked \u2014 see \u00a76) and tars the home volume into `~/agent-workspaces/snapshots/` (0700); `destroy` removes the container, keeps code and home unless explicitly purged. Credentials for the agent CLIs live in the home volume, so logins survive container re-creation.'))
story.append(P('**Tier-2 lifecycle.** `base` (once): download + SHA512-verify the official cloud image \u2192 golden overlay \u2192 cloud-init (packages via the host proxy, the nftables ruleset, subuid ranges, linger, package upgrade) \u2192 transfer + `podman load` the agent image \u2192 confirmed shutdown \u2192 freeze (refusing to replace the golden while overlay VMs exist). `create <name>` (seconds): copy-on-write overlay of golden + boot + container start inside; `verify <name>` asserts the Tier-2 isolation guarantees inside the VM. Backing-file sharing makes overlays instant; the flip side \u2014 a poisoned golden poisons all overlays \u2014 is why hardening \u00a74 recommends rebuilding golden per trust boundary.'))

# ---- 6. Component specifications
story += heading('6. Component specifications')
story.append(P('**Image contents** (`files/Containerfile`, all pins verified 2026-11-05): Debian trixie-slim base (digest-pinned); Python 3.13 + venv + dev headers; Node 24 (NodeSource, key fingerprint verified); Bun 1.3.14 (pinned installer tag); pnpm 12; uv 0.13.7; git/git-lfs; ripgrep, fd, jq, tmux, socat, openssh-client; build-essential + libssl/zlib/sqlite headers; SQLite; system Chromium 156 + fonts; Playwright 1.64.1 (Node *and* Python, shared browser revisions) baked to `/opt/ms-playwright`; agent-browser 0.41.2 with its Chrome baked to `/opt/agent-browser-data`; claude-code 2.1.318, codex 0.166.0, opencode 1.19.5; `NODE_USE_ENV_PROXY=1`; non-root `dev` (uid 1000); `sleep infinity` as PID 1. Result: ~3.5-4 GB image (~2 GB of it the unpacked `/opt` browser bake; the reference environment\u2019s Playwright-only cache was 613 MB), ~2 GB RAM per active workspace at idle-to-moderate load.'))
story += table_block(
    ['Layer', 'Pinned version', 'Why it is there'],
    [
        ['python3.13 + venv + dev', 'trixie 3.13.5', 'system Python for the distro; venv package is the documented trixie gotcha'],
        ['nodejs', '24.x (NodeSource `node_24.x`)', 'budget-wiser floor is Node \u2265 24; matches reference environment'],
        ['bun', '1.3.14 (`BUN_VERSION` ARG, pinned installer tag)', "budget-wiser\u2019s primary runtime (\u2265 1.3)"],
        ['pnpm', '12.16.1', 'package manager of choice for agent workflows'],
        ['uv', '0.13.7', 'fast per-project Python envs; standalone binary'],
        ['playwright (node+py)', '1.64.1', "matches budget-wiser\u2019s pin \u2192 shared browser revision, no re-download"],
        ['agent-browser', '0.41.2', 'accessibility-snapshot browser driving for agents (own Chrome 157)'],
        ['claude-code / codex / opencode', '2.1.318 / 0.166.0 / 1.19.5', 'the three agent CLIs, all `npm -g` installable, no Node runtime needed at their own runtime'],
        ['chromium', 'trixie 156', 'system browser + shared library base for both browser ecosystems'],
        ['ripgrep/fd/jq/socat/tmux', 'trixie packaged', 'agent ergonomics (search, JSON, port/probe, sessions)'],
    ],
    [0.26, 0.28, 0.46],
    'Table 3 \u2014 Image layers and their justification.', font=8.5)
story.append(P('**Egress policy** (`files/squid/allowlist.txt`): Debian mirrors; runtime installers (NodeSource, nodejs.org, astral.sh, bun.sh); registries (npm, yarn, PyPI); git hosts (GitHub, GitLab \u2014 leading-dot entries cover subdomain CDNs); Prisma engine binaries (`binaries.prisma.sh`, needed by the representative workload); Playwright CDN; the AI provider APIs; two verification domains. Squid `dstdomain` semantics: a leading dot matches subdomains, a bare domain is an EXACT match, `*.` is not a wildcard and is rejected by `allow`. Squid resolves DNS (workspaces never need it). Adding a domain: one command, both tiers, restart included \u2014 and every change is `squid -k parse`-validated before the gateway restarts.'))
story.append(P('**Ephemeral CI profile** (`scripts/45-ci-run.sh` + `files/ci-setup.sh`): single-shot containers from the same image \u2014 CI env, shared package caches, per-run isolation self-audit, artifact export, walltime timeout, orphan reaper. Full design in \u00a712.'))
story.append(P('**Resource budget** (16-32 GB host): gateway ~50 MB; each Tier-1 workspace default 6 GB/4 CPU cap (per-container) inside a user-slice budget; one Tier-2 VM 6 GB/4 vCPU by default. Comfortable: 2-4 active workspaces + 1 VM on 32 GB; 1-2 workspaces on 16 GB.'))
story.append(P('**Secrets plumbing.** Host file `~/.config/agent-sandbox/workspaces/<n>.env` (0600, never committed, never in an image) \u2192 `--env-file` at `podman run`. Agent CLI auth tokens live inside the home volume only. Snapshot caveat (verified against podman 5.4 source): `podman commit` copies the container\u2019s environment into the image config \u2014 `40-workspace.sh snapshot` therefore blanks every env-file key from the committed image; rotate keys after snapshotting a workspace that had live secrets, and never distribute `ws-snap-*` images. Tier-2 env files live inside the VM (`~/.config/agent-sandbox/`), so host compromise of the env dir does not automatically include VM workspaces\u2019 keys.'))

# ---- 7. Representative workload fit
story += heading('7. Representative workload fit \u2014 budget-wiser')
story.append(P('The chosen reference repo stresses every axis of the design: Next.js 16 + React 19 need Node \u2265 24 (or Bun \u2265 1.3) \u2014 both provided; Prisma 6 + SQLite needs libssl/sqlite \u2014 provided; `bun install` needs registry.npmjs.org \u2014 allowlisted \u2014 and, because budget-wiser enables Prisma\u2019s install scripts, it also fetches engine binaries from `binaries.prisma.sh` (allowlisted for exactly that reason; run the acceptance path to confirm the full domain set); `db:push/db:seed` are local file operations once the engines are present; Vitest runs offline; Playwright E2E launches Chromium against `localhost` \u2014 covered by `no_proxy` and the baked browser; `agent-browser` verifies UI state via accessibility snapshots. Onboarding inside a workspace:'))
story += code_block([
    'scripts/40-workspace.sh create wiser --repo https://github.com/nordeim/budget-wiser.git',
    'scripts/40-workspace.sh shell wiser',
    '# in-workspace:',
    'bun install && bun run db:push && bun run db:seed && bun run gate   # lint+type+unit+build+smoke+e2e',
    'bun run dev &       # localhost:3000',
    'agent-browser open http://localhost:3000 && agent-browser snapshot -i',
    'bun run test:e2e    # Playwright, local server \u2014 no external egress needed',
])
story.append(P('`50-verify.sh` performs the first step (clone via proxy) as a standing check; the rest is the documented user acceptance path.'))

# ---- 8. Security analysis
story += heading('8. Security analysis')
story.append(P('**Guarantees enforced by construction:** workspace processes run as non-root with zero capabilities, no privilege escalation, and cgroup caps; the only route off the host user\u2019s network namespace is Squid with a domain allowlist (403 + logged for everything else); external DNS is unavailable; no host path is writable inside a workspace except the project dir. Be honest about what that means: the bind mount shares YOUR uid, so a workload-user escape reaches your own files everywhere \u2014 not just the project dir. That is the same trust level as running the code by hand, which is precisely the Tier-1 contract; code you do not trust that far belongs in Tier 2. Host-executed persistence is also in scope: payloads planted in `.git/hooks` or package scripts run the next time YOU run host tooling against the mount \u2014 treat the mount as workload-owned. Tier-2 adds a full VM boundary and keeps all host paths out entirely.'))
story.append(P('**Verified, with caveats stated:** rootless defined-network NAT egress is a standard podman 5 capability and the `--internal` semantics are documented (netavark backend \u2014 preflight --post checks it); if rootless NAT misbehaves, debug netavark/pasta \u2014 there is deliberately NO rootful-gateway fallback, because workspaces on an `--internal` network cannot reach host loopback by design, and moving them to a routed network would break invariant 3. Chromium-family browsers do not reliably honor proxy env vars in every launch mode \u2014 external-page browsing via agent-browser is therefore a SOFT check with the explicit per-project Playwright proxy option documented; local dev-server testing (the dominant agent flow) is unaffected and hard-verified.'))
story.append(P('**Known residual risks** (by tier, see \u00a72 table and hardening \u00a76): shared kernel for Tier 1; workload-user escape = host user (keep-id; the tier discipline is the answer); host-side persistence vectors via the shared mount (`.git/hooks` etc.); supply chain of allowlisted domains AND of build-time endpoints (installers, npm transitives \u2014 see D8); allowed-channel exfiltration; side channels on shared hardware. The design\u2019s answer to the first two is the tier switch, to the third is allowlist governance + your normal package review, to the rest is stated scope.'))

# ---- 9. Operational characteristics
story += heading('9. Operational characteristics, logging & audit')
story.append(P('**Timing profile** (mid-range host): image build 5-15 min (first) / seconds (cached); workspace create ~3 s + first `seed-playwright-browsers` (< 1 s); workspace `restart` ~2 s; gateway start ~1 s; Tier-2 golden build 15-30 min (one-time); Tier-2 overlay create ~40 s to SSH. A CI run adds ~5-8 s of overhead around the command itself (container create + browser seeding + isolation self-audit); artifact copying is size-dependent.'))
story.append(P('**What happens on reboot:** linger + the gateway Quadlet bring the proxy back automatically (the generator applies `[Install]` at daemon-reload \u2014 `systemctl --user enable` is never used on generated units). Workspaces have NO restart policy: after a host reboot every workspace is stopped, and `40-workspace.sh start <name>` resumes it \u2014 a deliberate choice: agents should not auto-resume unfinished work unattended. VMs do not auto-start (their qemu processes are user-managed, not systemd units \u2014 keep it that way unless you add units yourself).'))
story.append(P('**Audit trail:** Squid access logs are the egress audit record \u2014 one line per proxied request and per denial. Container path: `journalctl --user -u agent-gateway.service` (or `podman logs agent-gateway`); Tier-2 host path: `/var/log/squid/access.log`. Answering "did workspace X contact domain Y?" is a one-line grep. Retention is your host\u2019s journald/logrotate policy \u2014 size the logs to your compliance needs.'))
story.append(P('**Host maintenance:** Debian security updates apply normally (host packages are outside all sandboxes). After a host kernel update + reboot, re-run `50-verify.sh` before resuming untrusted work \u2014 the suite is cheap and the kernel is the Tier-1 boundary.'))

# ---- 10. Design questions
story += heading('10. Design questions you will ask')
story.append(P('**Why not Claude Code\u2019s own sandbox / Codex\u2019s built-in sandboxing?** Both CLIs ship process-level sandboxes (seccomp/Landlock/namespace wrappers). They harden *the CLI\u2019s own tool calls* \u2014 but the user may run other agents, ad-hoc commands, or a different CLI version; and process sandboxes do not provide resource caps, egress allowlists, or a reproducible environment. Caveat: those sandbox modes generally need privileges this container deliberately drops, so expect them to run in a degraded or disabled mode INSIDE a workspace \u2014 the workspace boundary is the one that counts, and agent-internal sandboxing remains an optional extra layer, never the boundary.'))
story.append(P('**Why is the gateway a container instead of host squid for Tier 1?** Rootless containers on an internal network cannot reach host loopback; the dual-homed gateway container keeps the entire Tier-1 plane inside the unprivileged user realm (no root-owned moving parts) and makes the whole thing portable via Quadlet. Tier 2 does use host squid \u2014 VMs reach it via QEMU\u2019s 10.0.2.2 mapping, which lands on loopback.'))
story.append(P('**Why allow example.com but not a general docs allowlist?** Every line is a standing grant to untrusted code. Two inert verification domains are shipped; anything else is a deliberate, reviewable policy decision via `30-gateway.sh allow`. Agents that need docs access get it the same way \u2014 explicitly, observably, revocably.'))
story.append(P('**Can a workspace use Docker/Compose inside?** No \u2014 deliberately. Nested container runtimes need privileges this design refuses to grant. Projects needing multi-service topologies should use podman-in-VM (Tier 2, where rootless podman IS available inside the VM) or the host-side scripts.'))

# ---- 11. Runbooks
story += heading('11. Runbooks')
story.append(P('**Day-0 (install, ~25-40 min including image build):** `00-preflight.sh` \u2192 `10-host-bootstrap.sh [--tier2]` \u2192 re-login if kvm group added \u2192 `00-preflight.sh --post` \u2192 `20-build-image.sh` \u2192 `30-gateway.sh up` \u2192 `50-verify.sh` \u2192 (optional) `60-tier2-microvm.sh base`.'))
story.append(P('**Day-1 (new project):** `40-workspace.sh create <name> [--repo URL]` \u2192 edit env file \u2192 `restart <name>` \u2192 `shell <name>` \u2192 run the agent CLI.'))
story.append(P('**Day-2 (ongoing):** allowlist changes (`30-gateway.sh allow`); tool refresh (bump ARG \u2192 rebuild \u2192 re-verify \u2192 `restart` workspaces); snapshots before risky agent sessions; `podman system df` housekeeping; allowlist review; rebuild Tier-2 golden between trust boundaries.'))

# ---- 12. Ephemeral CI profile
story += heading('12. Ephemeral CI profile')
story.append(P('The roadmap\u2019s "ephemeral CI profiles" item, delivered. The insight that keeps it cheap: CI here is not a new environment but a new *consumption mode* of the one that already exists.', lede))
story += table_block(
    ['Mode', 'Tool', 'Lifecycle', 'Home', 'Code'],
    [
        ['Interactive workspace', '`40-workspace.sh`', 'persistent (stop/start/restart)', 'named volume `agent-home-<n>`', 'host bind `~/agent-workspaces/<n>`'],
        ['Ephemeral CI run', '`45-ci-run.sh`', 'one command, then destroyed', 'container layer (or run-local bind with `--read-only-rootfs`)', 'run dir, or `--src` checkout'],
        ['Container-in-VM', '`60-tier2-microvm.sh`', 'per engagement', 'inside the VM', 'VM disk'],
    ],
    [0.19, 0.21, 0.22, 0.22, 0.16],
    'Table 4 \u2014 One image, three consumption modes.', font=8.5)
story.append(P('**Runner.** `45-ci-run.sh run [--repo URL | --src DIR] [--timeout S] -- <command...>` creates a single-shot container that is hardened *exactly* like a workspace \u2014 keep-id, cap-drop=ALL, no-new-privileges, `agent-internal` only, env-file secrets, pids/memory/cpu caps \u2014 plus a walltime `timeout` (default 3600 s). The command streams live *and* is captured to `artifacts/console.log` (repository URLs are redacted before they reach any log or summary). Teardown always follows the run (`--keep-on-failure` opts out for debugging); the post-run artifact copier is symlink-contained (`cp -rP` + realpath checks) because the run directory is workload-controlled; `reap` removes orphans and stale run dirs past a TTL; `list` prints past runs from their summaries; `cache` wipes the shared package caches. `jq` on the host is required (bootstrap installs it; the runner checks upfront).'))
story.append(P('**In-container preamble.** `files/ci-setup.sh` is bind-mounted in (image unchanged \u2014 D6 holds): it sets `CI=true` (pnpm then defaults to a frozen lockfile in CI), points npm/pip/uv/bun/pnpm caches at the shared tree, seeds browsers, optionally shallow-clones `CI_REPO_URL`, then \u2014 before any workload code runs \u2014 **audits isolation**: uid 1000, zero caps, NoNewPrivs, direct egress must fail, external DNS must fail, the proxy must 403 a known-denied domain and 200 an allowlisted one; the run\u2019s pids/memory cgroup caps are recorded as evidence too (a `max` reading is reported, not failed \u2014 rootless cgroup delegation varies by host, so `50-verify.sh` treats the same condition as a soft warning; see troubleshooting \u00a75). Results land in `artifacts/isolation-audit.json`; any failure exits **66** without running the command. Every CI run therefore carries its own evidence that the sandbox guarantees held *for that run*.'))
story.append(P('**Artifacts.** `~/agent-workspaces/__ci/artifacts/<run-id>/` keeps `console.log`, `isolation-audit.json`, a schema\u2019d `run-summary.json` (exit code, duration, audit status, cache mode, copied files), and the report dirs the copier knows by default (`playwright-report`, `test-results`, `coverage`, `dist`, `build`, `junit.xml`; extend with `--artifact-path`, globs allowed).'))
story.append(P('**Caches and trust.** Shared caches are a host bind mount (`~/agent-workspaces/__ci/cache` \u2192 `/cache`) \u2014 deliberately *not* a named volume, because same-uid bind mounts are this design\u2019s proven primitive (D5); no orphan volumes can ever exist. The tree is shared writable state across runs: pnpm\u2019s own documentation makes exactly this point about its store, and the same reasoning applies to npm/pip/uv/bun caches. Same host, same user, same trust domain \u2014 fine for your own projects; `--no-cache-vol` gives a run cold, isolated caches when the source is less trusted, and hostile PR builds belong in Tier 2 (the same script runs inside the VM). CI mode changes consumption, never the trust tier.'))
story.append(P('**Naming.** Containers are `agent-__ci-<run-id>`, state lives under the `__ci/` subtree of the workspaces root. `40-workspace.sh`\u2019s `validate_name` reserves the `__` prefix, so CI containers cannot collide with interactive workspaces and `reap` cannot touch them \u2014 the same structural reservation the verify canary (`__verify`) uses.'))
story.append(P('**Representative run (budget-wiser gate):**'))
story += code_block([
    'scripts/45-ci-run.sh run --repo https://github.com/nordeim/budget-wiser.git \\',
    '    -- bash -lc \'bun install && bun run db:push && bun run db:seed && bun run gate\'',
    'scripts/45-ci-run.sh list',
])
story.append(P('Exit codes are a contract:'))
story += table_block(
    ['Exit', 'Meaning'],
    [
        ['0', 'ok \u2014 command succeeded, self-audit passed'],
        ['66', 'isolation audit failed \u2014 guarantees did not hold; command never ran'],
        ['124', 'walltime timeout reached'],
        ['125 / 126 / 127', 'podman-level error (image missing, name clash, runtime failure)'],
        ['any other', 'the command\u2019s own exit code, propagated'],
    ],
    [0.20, 0.80],
    'Table 5 \u2014 CI run exit-code contract.', font=9)
story.append(P('See `references/troubleshooting.md` \u00a79 for the failure playbook (including why `--skip-audit` is never a fix).'))

# ---- 13. Verification as specification
story += heading('13. Verification as specification')
story.append(P('`50-verify.sh` maps each guarantee to a check, and \u2014 crucially \u2014 encodes the *negative* tests as first-class requirements: direct egress must fail, external DNS must fail, non-allowlisted domains must 403. A green run is a reproducible evidence ledger (per-check PASS/FAIL with captured output), designed so an AI operator cannot honestly report "done" without it \u2014 and the escalation rule forbids weakening checks to force green. The CI profile extends the same idea to every single run: its self-audit is 50-verify\u2019s isolation section, in miniature, attached to each job\u2019s artifacts.'))

# ---- 14. Roadmap
story += heading('14. Roadmap')
story.append(P('Registry mode (local `podman push` target for team-shared images); ephemeral CI profiles \u2014 **delivered** (\u00a712); gVisor/Kata runtime option for Tier 1.5; DNS-level allowlisting in Tier 2 (dnsmasq allow-resolver); automated monthly golden rebuilds with drift reports. Each extension is a delta on this blueprint, not a redesign.'))

# ---------------------------------------------------------------- build
doc = TocDocTemplate(
    OUT, pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN, topMargin=MARGIN, bottomMargin=MARGIN,
    title='Agent Dev Sandbox \u2014 Comprehensive Blueprint',
    author='Z.ai', creator='Z.ai',
    subject='Secure, egress-restricted development environment blueprint for AI coding agents on Debian 13',
)
doc.multiBuild(story, onFirstPage=on_page, onLaterPages=on_page)
print('body written:', OUT)
