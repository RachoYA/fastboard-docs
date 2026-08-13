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


---

# Боевая установка: локальная модель + Telegram-бот

Так развёрнут сервер консультанта `89.232.184.218` (пользователь `racho`,
каталог `~/fastboard-docs`). Root-прав не требуется: всё работает на
пользовательском systemd (`systemctl --user`, включён `loginctl enable-linger`).

## Компоненты

| Юнит | Назначение |
|---|---|
| `gpu-ollama-tunnel.service` | SSH-туннель к Ollama на GPU-сервере → `127.0.0.1:11434` |
| `fastboard-bot.service` | Telegram-бот `scripts/telegram_bot.py` |
| `fastboard-docs-update.timer` | Ежедневный инкремент базы знаний в 03:00 |

Файлы юнитов — в [`deploy/user/`](user/), раскладываются деплой-скриптом
в `~/.config/systemd/user/`.

## Доступ к GPU-серверу

Модель живёт на отдельной машине с A100 и слушает только localhost, поэтому
сервер консультанта ходит к ней через SSH-туннель:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/gpu_tunnel -N ''      # на сервере консультанта
# публичный ключ — на GPU-сервер, с ограничением только на нужный порт:
# no-pty,permitopen="127.0.0.1:11434" ssh-ed25519 AAAA... fastboard-bot-tunnel
```

Проверка: `curl http://127.0.0.1:11434/api/tags`.

## Деплой из CI

`.github/workflows/deploy.yml` при пуше в `master` подключается по SSH и
выполняет [`remote_deploy.sh`](remote_deploy.sh). Секреты репозитория:

| Секрет | Значение |
|---|---|
| `DEPLOY_HOST` | адрес сервера консультанта |
| `DEPLOY_USER` | пользователь SSH |
| `DEPLOY_SSH_KEY` | приватный ключ деплоя (публичный — в `~/.ssh/authorized_keys` на сервере) |

Ручной прогон того же сценария:

```bash
bash deploy/remote_deploy.sh          # на сервере
```

Деплой не трогает `.env`, `vectordb/`, `logs/` и `state/` — они живут только на сервере.

## Первичная индексация

```bash
./.venv/bin/python scripts/scrape_and_index.py --full
```
