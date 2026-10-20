#!/usr/bin/env bash
# Разовая настройка сервера консультанта под root:
#   - системные юниты из deploy/system/ в /etc/systemd/system;
#   - право деплоя (deploy/remote_deploy.sh) перезапускать бота и веб-API без пароля;
#   - с аргументом-доменом: nginx и сертификат Let's Encrypt для API Фиби.
#
#   sudo bash deploy/system/install.sh                   # юниты и право на перезапуск
#   sudo bash deploy/system/install.sh fibi.grachia.ru   # то же + nginx и сертификат
#
# Запускать повторно безопасно, а после изменения юнитов в репозитории нужно:
# деплой без root их не ставит и в таком случае останавливается с подсказкой.
set -euo pipefail

[ "$(id -u)" -eq 0 ] || { echo "Запускайте через sudo: sudo bash $0 $*"; exit 1; }

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_USER=racho   # пользователь и пути зашиты в юнитах — как на боевом сервере
DOMAIN="${1:-}"

echo "→ systemd-юниты"
install -m 0644 "$HERE"/*.service "$HERE"/*.timer /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now gpu-ollama-tunnel.service \
    fastboard-docs-update.timer fastboard-watchdog.timer fastboard-backup.timer
systemctl enable fastboard-bot.service fastboard-web.service

echo "→ право деплоя перезапускать бота и веб-API"
tmp=$(mktemp)
cat > "$tmp" <<EOF
# Ставит fastboard-docs/deploy/system/install.sh: деплой перезапускает свои службы без пароля
$APP_USER ALL=(root) NOPASSWD: /usr/bin/systemctl restart fastboard-bot.service, /usr/bin/systemctl restart fastboard-web.service
EOF
visudo -cqf "$tmp"
install -m 0440 "$tmp" /etc/sudoers.d/fastboard-deploy
rm -f "$tmp"

echo "→ перезапуск бота и веб-API"
systemctl restart fastboard-bot.service fastboard-web.service
for _ in $(seq 1 30); do
    curl -fsS -m 5 http://127.0.0.1:8080/health >/dev/null 2>&1 && break
    sleep 2
done
curl -fsS -m 5 http://127.0.0.1:8080/health \
    || { echo; echo "!! веб-API не отвечает"; journalctl -u fastboard-web.service -n 40 --no-pager; exit 1; }
echo
systemctl is-active --quiet fastboard-bot.service \
    || { echo "!! бот не запустился"; journalctl -u fastboard-bot.service -n 40 --no-pager; exit 1; }

if [ -z "$DOMAIN" ]; then
    echo "✓ Готово. Публичный адрес: sudo bash $0 <домен>"
    exit 0
fi

SITE=/etc/nginx/sites-available/fibi
if [ ! -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
    echo "→ сертификат для $DOMAIN"
    # Пока сертификата нет, полный конфиг не пройдёт nginx -t: ставим временный
    # блок на 80-м порту, в который certbot добавит проверку домена
    cat > "$SITE" <<EOF
server {
    listen 80;
    server_name $DOMAIN;
    location / { return 404; }
}
EOF
    ln -sf "$SITE" /etc/nginx/sites-enabled/fibi
    nginx -t && systemctl reload nginx
    certbot certonly --nginx -d "$DOMAIN" --non-interactive --agree-tos \
        --deploy-hook "systemctl reload nginx"
fi

echo "→ nginx для $DOMAIN"
sed "s/__DOMAIN__/$DOMAIN/g" "$HERE/nginx-fibi.conf" > "$SITE"
ln -sf "$SITE" /etc/nginx/sites-enabled/fibi
nginx -t && systemctl reload nginx
sleep 1
curl -fsS -m 10 "https://$DOMAIN/health" \
    || { echo; echo "!! https://$DOMAIN/health не отвечает"; exit 1; }
echo
echo "✓ Готово: API Фиби доступен на https://$DOMAIN"
