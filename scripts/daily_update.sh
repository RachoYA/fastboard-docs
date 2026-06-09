#!/usr/bin/env bash
# Ежедневное инкрементальное обновление документации (для запуска на сервере).
# Подходит для cron и systemd. Логи пишутся в logs/.
set -euo pipefail

# Корень репозитория (на уровень выше каталога scripts/)
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Виртуальное окружение, если есть
if [ -d ".venv" ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
fi

# Переменные окружения из .env (если есть); иначе берутся из окружения процесса
if [ -f ".env" ]; then
    set -a
    # shellcheck disable=SC1091
    . ./.env
    set +a
fi

mkdir -p logs
LOG="logs/daily_$(date -u +%Y%m%d).log"

echo "=== $(date -u +%FT%TZ) старт инкрементального обновления ===" >> "$LOG"
python scripts/scrape_and_index.py "$@" >> "$LOG" 2>&1
echo "=== $(date -u +%FT%TZ) готово ===" >> "$LOG"
