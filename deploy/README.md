# Развёртывание ежедневного обновления на сервере

Ежедневный инкремент запускается на вашем сервере (не на GitHub). Состояние —
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
