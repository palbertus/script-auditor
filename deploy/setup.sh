#!/bin/bash
# One-shot setup script for Debian/Ubuntu VPS
# Run as root: bash setup.sh

set -e

APP_DIR="/opt/script-auditor"
SERVICE_USER="www-data"

echo "==> Installing system dependencies..."
apt-get update -qq
apt-get install -y python3 python3-pip python3-venv nginx git \
    # Playwright/Chromium system libs (covers most of them):
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libasound2 libpango-1.0-0 libpangocairo-1.0-0

echo "==> Creating app directory..."
mkdir -p "$APP_DIR"
mkdir -p /var/log/script-auditor

echo "==> Copying app files..."
cp -r . "$APP_DIR/"

echo "==> Creating Python virtualenv..."
python3 -m venv "$APP_DIR/venv"
"$APP_DIR/venv/bin/pip" install --upgrade pip -q
"$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt" -q

echo "==> Installing Playwright Chromium browser..."
PLAYWRIGHT_BROWSERS_PATH="$APP_DIR/.playwright" \
    "$APP_DIR/venv/bin/python" -m playwright install chromium
PLAYWRIGHT_BROWSERS_PATH="$APP_DIR/.playwright" \
    "$APP_DIR/venv/bin/python" -m playwright install-deps chromium

echo "==> Setting permissions..."
chown -R "$SERVICE_USER:$SERVICE_USER" "$APP_DIR"
chown -R "$SERVICE_USER:$SERVICE_USER" /var/log/script-auditor

echo "==> Installing systemd service..."
cp deploy/script-auditor.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable script-auditor
systemctl start script-auditor

echo "==> Configuring Nginx..."
cp deploy/nginx.conf /etc/nginx/sites-available/script-auditor
ln -sf /etc/nginx/sites-available/script-auditor /etc/nginx/sites-enabled/script-auditor
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

echo ""
echo "✓ Done. App running at http://$(hostname -I | awk '{print $1}')"
echo "  Logs: journalctl -u script-auditor -f"
