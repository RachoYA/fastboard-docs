#!/usr/bin/env bash
# Сторож: проверяет, что бот жив и канал к модели на месте.
# Запускается таймером раз в 5 минут (deploy/user/fastboard-watchdog.timer).
#
# При сбое пишет в журнал и, если задан ADMIN_CHAT_ID, шлёт сообщение в Telegram.
# Повторные сообщения об одной и той же поломке не шлются чаще раза в час —
# иначе при долгом сбое админ получит 12 сообщений в час и перестанет их читать.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
STATE_DIR="$ROOT/state"
LAST_ALERT="$STATE_DIR/watchdog-last-alert"
ALERT_COOLDOWN=3600

# .env читаем только ради токена и ADMIN_CHAT_ID
if [ -f .env ]; then
    TELEGRAM_BOT_TOKEN=$(grep -E '^TELEGRAM_BOT_TOKEN=' .env | cut -d= -f2- | tr -d '"')
    ADMIN_CHAT_ID=$(grep -E '^ADMIN_CHAT_ID=' .env | cut -d= -f2- | tr -d '"' || true)
    OLLAMA_URL=$(grep -E '^OLLAMA_URL=' .env | cut -d= -f2- | tr -d '"' || true)
fi
OLLAMA_URL="${OLLAMA_URL:-http://127.0.0.1:11434}"

problems=()

systemctl --user is-active --quiet fastboard-bot.service \
    || problems+=("бот не запущен (fastboard-bot.service)")
systemctl --user is-active --quiet gpu-ollama-tunnel.service \
    || problems+=("туннель к GPU не поднят (gpu-ollama-tunnel.service)")
curl -fsS -m 15 "$OLLAMA_URL/api/version" >/dev/null 2>&1 \
    || problems+=("модель недоступна: $OLLAMA_URL не отвечает")

# Туннель, который часто переподключается, формально «active», но связь рвётся
restarts=$(systemctl --user show gpu-ollama-tunnel.service -p NRestarts --value 2>/dev/null || echo 0)
prev_restarts=$(cat "$STATE_DIR/watchdog-restarts" 2>/dev/null || echo "$restarts")
if [ "$restarts" -gt $((prev_restarts + 3)) ]; then
    problems+=("туннель переподключался $((restarts - prev_restarts)) раз с прошлой проверки")
fi
mkdir -p "$STATE_DIR"
echo "$restarts" > "$STATE_DIR/watchdog-restarts"

# Диск: база и логи растут, а места на сервере немного
free_pct=$(df --output=pcent "$ROOT" | tail -1 | tr -dc '0-9')
[ "${free_pct:-0}" -lt 92 ] || problems+=("диск заполнен на ${free_pct}%")

if [ ${#problems[@]} -eq 0 ]; then
    echo "$(date -u +%FT%TZ) всё в порядке: бот, туннель и модель на месте"
    exit 0
fi

message="⚠️ Консультант Fastboard: $(printf '%s; ' "${problems[@]}")"
echo "$(date -u +%FT%TZ) $message" >&2

now=$(date +%s)
last=$(cat "$LAST_ALERT" 2>/dev/null || echo 0)
if [ -n "${ADMIN_CHAT_ID:-}" ] && [ $((now - last)) -ge "$ALERT_COOLDOWN" ]; then
    curl -sS -m 20 "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d "chat_id=${ADMIN_CHAT_ID}" --data-urlencode "text=${message}" >/dev/null \
        && echo "$now" > "$LAST_ALERT"
fi
exit 1
