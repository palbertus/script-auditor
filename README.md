# Script Auditor

Detect every JavaScript script loaded on a webpage — including tags **injected by Google Tag Manager after page load** — and identify their vendor (GA4, Hotjar, Facebook Pixel, HubSpot, etc.).

![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)
![Playwright](https://img.shields.io/badge/playwright-chromium-green)
![Flask](https://img.shields.io/badge/flask-3.x-lightgrey)

---

## Features

- 🔍 Detects **all scripts**: inline, external, and dynamically injected
- 🏷️ **GTM-aware**: flags scripts loaded by Google Tag Manager
- 🏢 **50+ vendors** identified: Google, Meta, Hotjar, HubSpot, Segment, Intercom, Amplitude, Sentry, Stripe, OneTrust, and more
- 🌐 **Web UI** with live progress, vendor breakdown, and filterable script table
- 💻 **CLI mode** for terminal use and batch processing
- 📄 JSON output for every scan

---

## Quick start (local)

### 1. Install dependencies

```bash
pip3 install -r requirements.txt
python3 -m playwright install chromium
```

### 2. Run the web app

```bash
python3 app.py
```

Open **http://127.0.0.1:8080** in your browser.

### 3. Or use the CLI

```bash
# Single URL
python3 audit_scripts.py https://example.com --verbose

# Multiple URLs from file
python3 audit_scripts.py --file urls.txt --output results.json

# Options
python3 audit_scripts.py --help
```

---

## CLI reference

```
python3 audit_scripts.py <url>            Single URL
python3 audit_scripts.py --file FILE      Batch mode (one URL per line)
python3 audit_scripts.py --output FILE    Output JSON path (default: output/audit_TIMESTAMP.json)
python3 audit_scripts.py --timeout N      Seconds to wait per URL (default: 30)
python3 audit_scripts.py --no-headless    Show browser window (debug)
python3 audit_scripts.py --verbose        Print full script table to terminal
```

### Output format

```json
{
  "url": "https://example.com",
  "scanned_at": "2026-02-18T10:00:00Z",
  "gtm_detected": true,
  "scripts": [
    {
      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-XXXX",
      "name": "gtm.js",
      "vendor": "Google Tag Manager",
      "via_gtm": false,
      "type": "external"
    },
    {
      "url": "https://static.hotjar.com/c/hotjar-XXXXX.js",
      "name": "hotjar-XXXXX.js",
      "vendor": "Hotjar",
      "via_gtm": true,
      "type": "external"
    }
  ]
}
```

---

## Deploy on a Linux VPS (Debian/Ubuntu)

### One-shot setup

```bash
# On your VPS as root
git clone https://github.com/palbertus/script-auditor.git /tmp/script-auditor
cd /tmp/script-auditor
bash deploy/setup.sh
```

This installs Python, Nginx, Gunicorn, Playwright + Chromium, configures a systemd service, and starts the app.

### What the stack looks like

```
Internet → Nginx (port 80/443) → Gunicorn (127.0.0.1:8080) → Flask app
                                                              └→ Playwright Chromium (per request)
```

### Management commands

```bash
systemctl status script-auditor     # check status
systemctl restart script-auditor    # restart after code changes
journalctl -u script-auditor -f     # live logs
```

### Add HTTPS (Let's Encrypt)

```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d your-domain.com
```

---

## How it works

1. **Playwright** launches headless Chromium and intercepts all network requests before navigation
2. Navigates with `wait_until="networkidle"` — gives GTM time to fire its tags — then waits an extra 2 seconds for late-firing tags
3. **Diffs** network-captured script requests against the DOM's `<script src>` snapshot:
   - Scripts in the DOM = loaded from HTML directly
   - Scripts captured on the network but **not** in the DOM = injected dynamically (flagged `via_gtm: true` when GTM is present)
4. Inline `<script>` blocks are scanned for vendor fingerprints (`fbq(`, `gtag(`, `_hsq`, etc.)
5. Every script URL is matched against an ordered list of **50+ vendor patterns**

---

## Vendor coverage

| Category | Vendors |
|---|---|
| Analytics | Google Analytics (UA + GA4), Mixpanel, Amplitude, Heap, Segment |
| Tag Management | Google Tag Manager |
| Marketing | Facebook Pixel, LinkedIn Insight, Twitter/X Pixel, TikTok Pixel, Pinterest Tag, Google Ads |
| Heatmaps | Hotjar, Microsoft Clarity, Crazy Egg, Lucky Orange, FullStory |
| CRM / Support | HubSpot, Intercom, Drift, Zendesk, Crisp |
| Product Analytics | Pendo |
| Error Tracking | Sentry, Datadog, New Relic |
| Payments | Stripe |
| Consent (CMP) | OneTrust, Cookiebot, Didomi |
| CDN Libraries | jQuery, Google Hosted Libs, Cloudflare CDNJS, jsDelivr, unpkg |

---

## Project structure

```
script-auditor/
├── app.py                  # Flask web app (SSE streaming)
├── audit_scripts.py        # Core audit engine + CLI
├── vendor_map.py           # Vendor pattern matching
├── gunicorn.conf.py        # Production server config
├── requirements.txt
├── templates/
│   └── index.html          # Single-page UI
└── deploy/
    ├── setup.sh            # VPS install script
    ├── script-auditor.service  # systemd unit
    └── nginx.conf          # Nginx reverse proxy
```

---

## Requirements

- Python 3.9+
- Chromium (installed via `python3 -m playwright install chromium`)
- ~300 MB disk space for the Chromium binary
