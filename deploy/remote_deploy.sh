#!/usr/bin/env bash
# Развёртывание на сервере. Запускается из CI по SSH (см. .github/workflows/deploy.yml),
# либо вручную: bash deploy/remote_deploy.sh
#
# Идемпотентно: обновляет код до origin/master, ставит зависимости, раскладывает
# systemd-юниты пользователя и перезапускает бота. Файл .env, векторная база и
# логи живут на сервере и деплоем не затрагиваются.
set -euo pipefail

APP_DIR="${APP_DIR:-$HOME/fastboard-docs}"
REPO="${REPO:-https://github.com/RachoYA/fastboard-docs.git}"
BRANCH="${BRANCH:-master}"

if [ ! -d "$APP_DIR/.git" ]; then
    echo "→ Клонирую $REPO в $APP_DIR"
    git clone --quiet "$REPO" "$APP_DIR"
fi
cd "$APP_DIR"

echo "→ Обновляю код до origin/$BRANCH"
git fetch --quiet origin "$BRANCH"
git reset --hard --quiet "origin/$BRANCH"
git --no-pager log --oneline -1

echo "→ Зависимости"
[ -d .venv ] || python3 -m venv .venv
./.venv/bin/pip install --quiet --upgrade pip
./.venv/bin/pip install --quiet -r requirements.txt
chmod +x scripts/daily_update.sh scripts/telegram_bot.py scripts/watchdog.sh scripts/backup.sh

if [ ! -f .env ]; then
    echo "!! Нет $APP_DIR/.env — скопируйте .env.example и заполните (токен бота, адрес модели)."
    exit 1
fi

echo "→ systemd-юниты пользователя"
mkdir -p "$HOME/.config/systemd/user"
cp deploy/user/*.service deploy/user/*.timer "$HOME/.config/systemd/user/"
systemctl --user daemon-reload
systemctl --user enable --now gpu-ollama-tunnel.service
systemctl --user enable --now fastboard-docs-update.timer
systemctl --user enable --now fastboard-watchdog.timer
systemctl --user enable --now fastboard-backup.timer
systemctl --user enable fastboard-bot.service
systemctl --user restart fastboard-bot.service

echo "→ Проверка"
sleep 6
systemctl --user is-active gpu-ollama-tunnel.service >/dev/null \
    || { echo "!! Туннель к GPU не поднялся"; systemctl --user status gpu-ollama-tunnel.service --no-pager -l | tail -20; exit 1; }
curl -fsS -m 15 http://127.0.0.1:11434/api/version >/dev/null \
    || { echo "!! Ollama на GPU-сервере недоступна через туннель"; exit 1; }
systemctl --user is-active fastboard-bot.service >/dev/null \
    || { echo "!! Бот не запустился"; journalctl --user -u fastboard-bot.service -n 40 --no-pager; exit 1; }

echo "✓ Готово: бот работает, модель доступна"
journalctl --user -u fastboard-bot.service -n 5 --no-pager
