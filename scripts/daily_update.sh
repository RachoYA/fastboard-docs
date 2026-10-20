#!/usr/bin/env bash
# Ежедневное инкрементальное обновление документации (для запуска на сервере).
# Подходит для cron и systemd. Логи пишутся в logs/.
set -euo pipefail

# Корень репозитория (на уровень выше каталога scripts/)
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Защита от параллельных запусков (cron + ручной запуск): ChromaDB
# PersistentClient не рассчитан на нескольких писателей одновременно.
# Перезапускаем скрипт под flock на собственном лок-файле.
LOCK="$ROOT/.daily_update.lock"
if [ "${_FB_LOCKED:-}" != "1" ]; then
    exec env _FB_LOCKED=1 flock -n "$LOCK" "$0" "$@"
fi

# Виртуальное окружение, если есть
if [ -d ".venv" ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
fi

# Переменные окружения берутся из .env (его читает python-dotenv внутри скрипта)
# либо из окружения процесса/systemd. Намеренно НЕ выполняем `source .env`,
# чтобы значения со спецсимволами/пробелами не ломали shell.

mkdir -p logs
LOG="logs/daily_$(date -u +%Y%m%d).log"

echo "=== $(date -u +%FT%TZ) старт инкрементального обновления ===" >> "$LOG"
python scripts/scrape_and_index.py "$@" >> "$LOG" 2>&1
echo "=== $(date -u +%FT%TZ) индексация завершена ===" >> "$LOG"

# Контроль качества сразу после обновления: проверки базы и эталонные вопросы.
# Падение проверок не считается провалом обновления — база уже обновлена,
# но в логе и в state/eval-report.json останется след. Провал ещё и уходит
# сообщением в ADMIN_CHAT_ID: с 23.09.2026 отсечка вопросов вне темы
# не работала четыре недели, а знал об этом только файл лога.
notify_admin() {
    local token chat
    token=$(grep -E '^TELEGRAM_BOT_TOKEN=' .env 2>/dev/null | cut -d= -f2- | tr -d '"' || true)
    chat=$(grep -E '^ADMIN_CHAT_ID=' .env 2>/dev/null | cut -d= -f2- | tr -d '"' || true)
    [ -n "$token" ] && [ -n "$chat" ] || return 0
    curl -sS -m 20 "https://api.telegram.org/bot${token}/sendMessage" \
        -d "chat_id=${chat}" --data-urlencode "text=$1" >/dev/null 2>&1 || true
}

echo "=== $(date -u +%FT%TZ) проверки качества ===" >> "$LOG"
EVAL_OUT=$(mktemp)
if ! python scripts/eval.py > "$EVAL_OUT" 2>&1; then
    echo "!! Проверки качества не пройдены" >> "$EVAL_OUT"
    failed=$(grep -E '❌|РЕГРЕССИЯ' "$EVAL_OUT" | head -15 | cut -c1-300 || true)
    notify_admin "⚠️ Консультант Fastboard: ночные проверки качества не пройдены
${failed:-подробности в логе}
Лог: $ROOT/$LOG"
fi
cat "$EVAL_OUT" >> "$LOG"
rm -f "$EVAL_OUT"

echo "=== $(date -u +%FT%TZ) готово ===" >> "$LOG"
