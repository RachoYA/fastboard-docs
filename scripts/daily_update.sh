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
# но в логе и в state/eval-report.json останется след, а регрессии видны сразу.
echo "=== $(date -u +%FT%TZ) проверки качества ===" >> "$LOG"
python scripts/eval.py >> "$LOG" 2>&1 || echo "!! Проверки качества не пройдены" >> "$LOG"

echo "=== $(date -u +%FT%TZ) готово ===" >> "$LOG"
