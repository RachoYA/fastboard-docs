#!/usr/bin/env python3
"""Планировщик ежедневной инкрементальной индексации (для Docker-контейнера).

Делает прогон при старте (инкремент; авто-полная пересборка, если база пуста),
затем запускает индексацию каждый день в час INDEX_HOUR_UTC.
"""

import os
import sys
import time
import logging
import subprocess
from datetime import datetime, timezone, timedelta

logging.basicConfig(
    format="%(asctime)s %(levelname)s scheduler: %(message)s", level=logging.INFO
)
log = logging.getLogger("scheduler")

INDEX_HOUR_UTC = int(os.environ.get("INDEX_HOUR_UTC", "3"))
SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scrape_and_index.py")


def run_index():
    log.info("Запуск индексации...")
    res = subprocess.run([sys.executable, SCRIPT], check=False)
    log.info("Индексация завершена (код %s)", res.returncode)


def seconds_until_next_run():
    now = datetime.now(timezone.utc)
    nxt = now.replace(hour=INDEX_HOUR_UTC, minute=0, second=0, microsecond=0)
    if nxt <= now:
        nxt += timedelta(days=1)
    return (nxt - now).total_seconds(), nxt


def main():
    log.info("Планировщик запущен. Ежедневный прогон в %02d:00 UTC.", INDEX_HOUR_UTC)
    run_index()  # первичный прогон при старте
    while True:
        delay, nxt = seconds_until_next_run()
        log.info("Следующий запуск: %s (через %.0f мин)", nxt.isoformat(), delay / 60)
        time.sleep(delay)
        run_index()


if __name__ == "__main__":
    main()
