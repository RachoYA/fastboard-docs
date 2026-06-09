# Развёртывание на сервере

Рекомендуемый способ — **Docker Compose** (бот + индексатор + ChromaDB).
Ниже также описан вариант без Docker (cron/systemd) только для индексатора.

## Вариант 0 (рекомендуемый). Docker Compose: бот + индексатор + ChromaDB

```bash
cd /opt/fastboard-docs
cp .env.example .env          # OPENROUTER_API_KEY, TELEGRAM_BOT_TOKEN
docker compose up -d --build

docker compose ps
docker compose logs -f bot          # логи бота
docker compose logs -f indexer      # логи индексации
```

Сервисы (`docker-compose.yml`):
- **chroma** — ChromaDB-сервер, данные в volume `chroma-data`.
- **bot** — Telegram-бот (polling), отвечает на вопросы пользователей.
- **indexer** — ежедневная инкрементальная индексация (`INDEX_HOUR_UTC`, по умолч. 03:00 UTC).

Полезное:
```bash
docker compose run --rm indexer python scripts/scrape_and_index.py --full   # ручная полная пересборка
docker compose restart bot
docker compose down                  # остановить (volume с базой сохранится)
```

> После первого успешного деплоя зафиксируйте версию образа `chromadb/chroma`
> в `docker-compose.yml` вместо `latest`.

---

## Только индексатор без Docker (cron/systemd)

Если Telegram-бот не нужен и достаточно ежедневно обновлять базу. Состояние —
`vectordb/`, `scrape_manifest.json` и markdown-файлы — хранится на диске и
переиспользуется между запусками, поэтому каждый день обрабатывается только
изменившаяся «дельта».

## Подготовка

```bash
cd /opt/fastboard-docs              # путь под себя
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                # впишите OPENROUTER_API_KEY
chmod +x scripts/daily_update.sh
```

## Вариант 1. cron

```cron
# crontab -e — ежедневно в 03:00
0 3 * * * /opt/fastboard-docs/scripts/daily_update.sh
```

Скрипт сам подхватит `.venv` и `.env`, а логи запишет в `logs/`.

## Вариант 2. systemd timer

```bash
sudo cp deploy/fastboard-docs-update.service /etc/systemd/system/
sudo cp deploy/fastboard-docs-update.timer   /etc/systemd/system/
# поправьте User= и пути в .service при необходимости
sudo systemctl daemon-reload
sudo systemctl enable --now fastboard-docs-update.timer

# проверка
systemctl list-timers fastboard-docs-update.timer
systemctl start fastboard-docs-update.service   # разовый прогон
journalctl -u fastboard-docs-update.service -n 50
```

## Ручной запуск

```bash
./scripts/daily_update.sh            # инкремент
./scripts/daily_update.sh --full     # полная пересборка
./scripts/daily_update.sh --prune    # удалять исчезнувшие страницы
```

Скрипт берёт `flock` на `.daily_update.lock`, поэтому параллельный запуск
(cron + ручной) безопасен — второй процесс просто завершится, не повредив
векторную базу.

## Ротация логов

Логи пишутся по файлу в день в `logs/` и не чистятся автоматически. Пример
`logrotate` (`/etc/logrotate.d/fastboard-docs`):

```
/opt/fastboard-docs/logs/*.log {
    weekly
    rotate 8
    compress
    missingok
    notifempty
}
```

