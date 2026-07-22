---
name: cloudflare-tunnel
description: |
  Add new local services to an existing Cloudflare Tunnel for secure public access. Use when you need to expose a local development server, web application, or service running on localhost to the public internet via Cloudflare's tunnel infrastructure.

  Prerequisites: cloudflared installed and authenticated, existing tunnel created.

  Triggers: "add tunnel", "expose local service", "cloudflare tunnel", "port forward", "public access to localhost", "expose localhost".
---

# Cloudflare Tunnel Service Management

Add new local services to an existing Cloudflare Tunnel for secure public access without opening ports or having a public IP.

## Overview

**What this skill does:** Adds a new localhost service to an existing Cloudflare Tunnel by:
1. Creating a DNS CNAME record for the subdomain
2. Adding an ingress rule to `~/.cloudflared/config.yml`
3. Restarting the systemd service to apply changes

**Prerequisites (already set up):**
- cloudflared installed: `/home/pete/.local/bin/cloudflared`
- Authenticated: `~/.cloudflared/` contains credentials
- Tunnel exists: `baking` (ID: `2784ef2b-a6b5-4c29-b1e5-5beaea4b5fd2`)
- Systemd service running: `cloudflared-tunnel.service`

---

## Current Configuration

### Tunnel Information

| Property | Value |
|----------|-------|
| **Tunnel Name** | `baking` |
| **Tunnel ID** | `2784ef2b-a6b5-4c29-b1e5-5beaea4b5fd2` |
| **Domain** | `jesspete.shop` |
| **Config File** | `~/.cloudflared/config.yml` |
| **Service** | `cloudflared-tunnel.service` |

### Active Services (as of 2026-03-26)

| Subdomain | Local Service | Port |
|-----------|---------------|------|
| `baking.jesspete.shop` | Baking E-commerce | 3000 |
| `artisan-baking.jesspete.shop` | Artisan Baking | 3001 |
| `atelier.jesspete.shop` | Atelier | 4173 |
| `ai-academy.jesspete.shop` | AI Academy | 5173 |

---

## Adding a New Service

### Step 1: Verify Prerequisites

```bash
# Check cloudflared is installed
which cloudflared
# Expected: /home/pete/.local/bin/cloudflared

# Check tunnel exists
cloudflared tunnel list
# Expected: baking tunnel with connections

# Check service is running
systemctl --user status cloudflared-tunnel.service
# Expected: active (running)
```

### Step 2: Create DNS Route

Create a CNAME record for the new subdomain:

```bash
# Syntax: cloudflared tunnel route dns <tunnel-name> <subdomain>.<domain>
cloudflared tunnel route dns baking <new-service>.jesspete.shop

# Example:
# cloudflared tunnel route dns baking myapp.jesspete.shop
# Output: Added CNAME myapp.jesspete.shop which will route to this tunnel tunnelID=2784ef2b-a6b5-4c29-b1e5-5beaea4b5fd2
```

### Step 3: Edit Config File

Add an ingress rule to `~/.cloudflared/config.yml`:

```bash
# View current config
cat ~/.cloudflared/config.yml

# Edit config
vi ~/.cloudflared/config.yml
```

**Add before the final `http_status:404` rule:**

```yaml
- hostname: <new-service>.jesspete.shop
  service: http://localhost:<port>
```

**Example config.yml structure:**

```yaml
tunnel: 2784ef2b-a6b5-4c29-b1e5-5beaea4b5fd2
credentials-file: /home/pete/.cloudflared/2784ef2b-a6b5-4c29-b1e5-5beaea4b5fd2.json

ingress:
  # Existing services
  - hostname: baking.jesspete.shop
    service: http://localhost:3000
  - hostname: artisan-baking.jesspete.shop
    service: http://localhost:3001
  - hostname: atelier.jesspete.shop
    service: http://localhost:4173
  - hostname: ai-academy.jesspete.shop
    service: http://localhost:5173

  # NEW SERVICE - add here
  - hostname: myapp.jesspete.shop
    service: http://localhost:8080

  # Catch-all must be last
  - service: http_status:404
```

### Step 4: Restart Service

Apply changes by restarting the systemd service:

```bash
# Restart the tunnel service
systemctl --user restart cloudflared-tunnel.service

# Verify it's running
systemctl --user status cloudflared-tunnel.service

# Check logs for errors
journalctl --user -u cloudflared-tunnel.service -n 20 --no-pager
```

### Step 5: Verify Tunnel

```bash
# Check tunnel connections
cloudflared tunnel info baking

# Test the new endpoint
curl -I https://<new-service>.jesspete.shop

# Or open in browser
xdg-open https://<new-service>.jesspete.shop
```

---

## Complete Example: Adding a New Service

**Scenario:** Add a new React app running on `localhost:8080` as `myapp.jesspete.shop`.

```bash
# 1. Create DNS route
$ cloudflared tunnel route dns baking myapp.jesspete.shop
2026-03-26T02:30:00Z INF Added CNAME myapp.jesspete.shop which will route to this tunnel tunnelID=2784ef2b-a6b5-4c29-b1e5-5beaea4b5fd2

# 2. Edit config file
$ vi ~/.cloudflared/config.yml
# Add:
#   - hostname: myapp.jesspete.shop
#     service: http://localhost:8080

# 3. Restart service
$ systemctl --user restart cloudflared-tunnel.service

# 4. Verify
$ systemctl --user status cloudflared-tunnel.service
● cloudflared-tunnel.service - Cloudflare Tunnel (Baking)
   Active: active (running)

# 5. Test
$ curl -I https://myapp.jesspete.shop
HTTP/2 200
```

---

## Quick Reference Commands

### Status Checks

```bash
# List all tunnels
cloudflared tunnel list

# Show tunnel details
cloudflared tunnel info baking

# Check service status
systemctl --user status cloudflared-tunnel.service

# View current config
cat ~/.cloudflared/config.yml

# Check service logs
journalctl --user -u cloudflared-tunnel.service -f
```

### Service Management

```bash
# Start service
systemctl --user start cloudflared-tunnel.service

# Stop service
systemctl --user stop cloudflared-tunnel.service

# Restart service
systemctl --user restart cloudflared-tunnel.service

# View logs
journalctl --user -u cloudflared-tunnel.service -n 50 --no-pager
```

### DNS Management

```bash
# Add DNS route
cloudflared tunnel route dns baking <subdomain>.jesspete.shop

# List DNS records for tunnel
cloudflared tunnel route dns baking --show-all

# Delete DNS route (if needed)
cloudflared tunnel route dns baking <subdomain>.jesspete.shop --overwrite-dns=false
```

---

## Troubleshooting

### Issue: Service Not Running

**Symptom:** `systemctl --user status` shows inactive or failed.

**Diagnosis:**
```bash
# Check service logs
journalctl --user -u cloudflared-tunnel.service -n 30 --no-pager

# Check if cloudflared binary exists
ls -la /home/pete/.local/bin/cloudflared

# Check if credentials file exists
ls -la ~/.cloudflared/2784ef2b-a6b5-4c29-b1e5-5beaea4b5fd2.json
```

**Solutions:**
```bash
# Ensure linger is enabled (allows service to run after logout)
loginctl enable-linger pete

# Reload systemd daemon
systemctl --user daemon-reload

# Restart service
systemctl --user restart cloudflared-tunnel.service
```

### Issue: DNS Not Resolving

**Symptom:** `curl: Could not resolve host`

**Diagnosis:**
```bash
# Check if DNS route was created
cloudflared tunnel route dns baking --show-all

# Verify DNS propagation
dig <subdomain>.jesspete.shop

# Check tunnel is connected
cloudflared tunnel info baking
```

**Solutions:**
```bash
# Re-create DNS route
cloudflared tunnel route dns baking <subdomain>.jesspete.shop

# Wait for DNS propagation (up to 5 minutes)
```

### Issue: Connection Refused

**Symptom:** `Unable to reach the origin service. dial tcp 127.0.0.1:<port>: connect: connection refused`

**Diagnosis:**
```bash
# Check if local service is running
ss -tlnp | grep <port>

# Or
netstat -tlnp | grep <port>

# Check service logs
journalctl --user -u cloudflared-tunnel.service -n 20 --no-pager | grep "<port>"
```

**Solutions:**
```bash
# Start the local service first
# Example: npm run dev -- --port 8080

# Verify service is accessible
curl http://localhost:<port>

# If service is on a different port, update config.yml
```

### Issue: Config Changes Not Applied

**Symptom:** Changes to `config.yml` not taking effect.

**Solutions:**
```bash
# Must restart service after config changes
systemctl --user restart cloudflared-tunnel.service

# Verify config syntax
cat ~/.cloudflared/config.yml

# Check service picked up changes
journalctl --user -u cloudflared-tunnel.service -n 10 --no-pager
```

### Issue: Error 203/EXEC

**Symptom:** `status=203/EXEC` in service status.

**Diagnosis:**
```bash
# Find actual cloudflared path
which cloudflared

# Check service file
cat ~/.config/systemd/user/cloudflared-tunnel.service
```

**Solution:**
```bash
# Update ExecStart path in service file
vi ~/.config/systemd/user/cloudflared-tunnel.service
# Change: ExecStart=/home/pete/.local/bin/cloudflared tunnel run baking

# Reload and restart
systemctl --user daemon-reload
systemctl --user restart cloudflared-tunnel.service
```

---

## Advanced: Multiple Tunnels

If you need multiple tunnels (rare):

```bash
# Create new tunnel
cloudflared tunnel create <new-tunnel-name>

# Create config file for new tunnel
vi ~/.cloudflared/config-<new-tunnel-name>.yml

# Create new systemd service
vi ~/.config/systemd/user/cloudflared-<new-tunnel-name>.service

# Enable and start
systemctl --user daemon-reload
systemctl --user enable cloudflared-<new-tunnel-name>.service
systemctl --user start cloudflared-<new-tunnel-name>.service
```

---

## Advanced: Non-HTTP Services

Cloudflare Tunnel supports SSH, RDP, and other protocols:

```yaml
# SSH access
- hostname: ssh.jesspete.shop
  service: ssh://localhost:22

# RDP access
- hostname: rdp.jesspete.shop
  service: rdp://localhost:3389

# TCP (any protocol)
- hostname: tcp.jesspete.shop
  service: tcp://localhost:9000
```

Note: Non-HTTP services require Cloudflare Access policies for security.

---

## Critical: Frontend API Proxy Configuration

### The Problem

When tunnelling an existing web application with a separate frontend and backend, the **frontend will fail to load API data** if:

1. Frontend is hardcoded to call `http://localhost:<backend-port>/api`
2. Browser resolves `localhost` to the **user's machine**, not the server
3. API calls fail with "Failed to load..." errors

### Why It Happens

```
Browser at https://myapp.example.com/
    │
    ├── Loads frontend HTML/JS ✅ (works)
    │
    └── JavaScript makes API call to VITE_API_URL
            │
            └── VITE_API_URL = http://localhost:8000/api/v1
                    │
                    └── Browser resolves localhost → user's machine
                            │
                            └── ❌ Connection refused (no backend there)
```

### Symptoms

- Frontend loads, displays "Failed to load {data}. Please try again later."
- Browser console shows `ERR_CONNECTION_REFUSED` to `localhost:<port>`
- Backend is running and healthy on the server
- Local development works perfectly

### Solution: Add Vite Proxy (Development Mode)

**Add to `vite.config.ts`:**

```typescript
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',  // Allow external connections
    port: 5173,
    allowedHosts: ['myapp.example.com', 'localhost', '127.0.0.1'],
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // Backend URL
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
```

**What this does:**
- Routes `/api/*` requests through the Vite dev server
- Vite forwards requests to the backend (same machine)
- Browser sees same-origin requests (no CORS issues)
- Works for both local and tunneled access

**After adding proxy:**
```
Browser → https://myapp.example.com/api/v1/courses/
                │
                └── Vite proxy forwards to localhost:8000
                        │
                        └── Backend responds ✅
```

### Verification Steps

After adding the proxy configuration:

```bash
# 1. Restart frontend dev server
cd /path/to/frontend && npm run dev

# 2. Test API through tunnel
curl -s https://myapp.example.com/api/v1/courses/ | jq '.success'
# Expected: true

# 3. Check browser console - no CORS or connection errors
```

### Production Considerations

The Vite proxy only works in development mode. For production:

**Option A: Path-Based Routing (Recommended)**

Add separate ingress rule for API:

```yaml
ingress:
  - hostname: myapp.example.com
    path: /api/*
    service: http://localhost:8000  # Backend
  - hostname: myapp.example.com
    service: http://localhost:5173  # Frontend
  - service: http_status:404
```

**Option B: Separate API Subdomain**

```yaml
ingress:
  - hostname: myapp.example.com
    service: http://localhost:5173  # Frontend
  - hostname: api.myapp.example.com
    service: http://localhost:8000  # Backend
  - service: http_status:404
```

Then update frontend env: `VITE_API_URL=https://api.myapp.example.com/api/v1`

### Checklist for New Web App Tunnel

When adding an existing web application to the tunnel:

- [ ] Verify frontend dev server runs on expected port
- [ ] Verify backend API server runs on expected port
- [ ] Add Vite proxy configuration (if dev mode)
- [ ] Update `allowedHosts` in Vite config to include tunnel domain
- [ ] Restart frontend dev server after config changes
- [ ] Test API endpoint through tunnel URL
- [ ] Check browser console for connection errors
- [ ] For production: configure path-based routing or separate API subdomain

### Related Documentation

- Vite Server Options: https://vite.dev/config/server-options.html#server-proxy
- Cloudflare Tunnel Path-Based Routing: https://developers.cloudflare.com/cloudflare-one/networks/cloudflare-tunnel/reference/configuration/

---

## Security Considerations

1. **All services are publicly accessible** by default
2. **Consider Cloudflare Access** for authentication:
   - Email OTP
   - GitHub OAuth
   - Google OAuth
   - Pin codes
3. **HTTPS is automatic** - no certificates needed
4. **Origin is hidden** - your localhost is not exposed
5. **DDoS protection** included with Cloudflare

---

## Reference Files

| File | Path | Purpose |
|------|------|---------|
| Config | `~/.cloudflared/config.yml` | Tunnel ingress rules |
| Credentials | `~/.cloudflared/<tunnel-id>.json` | Tunnel authentication |
| Service | `~/.config/systemd/user/cloudflared-tunnel.service` | Systemd unit file |
| Howto | `/home/project/cloudflare_tunnel_howto.txt` | Original documentation |

---

## References

- Official Docs: https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/
- Downloads: https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/downloads/
- YouTube Tutorial: https://www.youtube.com/watch?v=etluT8UC-nw

---

**Skill Version:** 1.1.0
**Last Updated:** March 26, 2026
**Status:** Production Ready ✅

---

## Related Analysis Reports

- [Cloudflare Tunnel API Integration Analysis Report](../../reports/Cloudflare_Tunnel_API_Integration_Analysis_Report.md) — Root cause analysis and solution options for frontend/backend tunneling issues
