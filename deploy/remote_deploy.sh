#!/usr/bin/env bash
# Развёртывание на сервере. Запускается из CI по SSH (см. .github/workflows/deploy.yml),
# либо вручную: bash deploy/remote_deploy.sh
#
# Обновляет код до origin/master, ставит зависимости и перезапускает бота и веб-API.
# Службы системные (deploy/system/). Ставит их и даёт деплою право на перезапуск
# разовая настройка под root: sudo bash deploy/system/install.sh — её же нужно
# повторить, если юниты в репозитории изменились. Файл .env, векторная база и
# логи живут на сервере и деплоем не затрагиваются.
set -euo pipefail

APP_DIR="${APP_DIR:-$HOME/fastboard-docs}"
REPO="${REPO:-https://github.com/RachoYA/fastboard-docs.git}"
BRANCH="${BRANCH:-master}"
SYSTEMCTL=/usr/bin/systemctl   # путь должен совпадать с правилом в /etc/sudoers.d/fastboard-deploy

if [ ! -d "$APP_DIR/.git" ]; then
    echo "→ Клонирую $REPO в $APP_DIR"
    git clone --quiet "$REPO" "$APP_DIR"
fi
cd "$APP_DIR"
ROOT_LOCK="$APP_DIR/.daily_update.lock"

echo "→ Обновляю код до origin/$BRANCH"
# Тот же замок, что берёт ночное обновление: git reset --hard поверх файлов,
# которые в этот момент переписывает индексатор, откатывает свежие страницы.
exec 9>"$ROOT_LOCK"
flock -w 600 9 || { echo "!! Не дождался окончания индексации"; exit 1; }
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

echo "→ Проверка кода"
# Синтаксическая ошибка уронила бы бота сразу после перезапуска
./.venv/bin/python -m py_compile scripts/*.py

echo "→ Юниты systemd"
stale=()
for f in deploy/system/*.service deploy/system/*.timer; do
    cmp -s "$f" "/etc/systemd/system/$(basename "$f")" || stale+=("$(basename "$f")")
done
[ -e /etc/sudoers.d/fastboard-deploy ] || stale+=("право на перезапуск (sudoers)")
if [ ${#stale[@]} -gt 0 ]; then
    echo "!! Код обновлён, но службы не перезапущены: на сервере устарело или"
    echo "   отсутствует: ${stale[*]}"
    echo "   Один раз под root: sudo bash $APP_DIR/deploy/system/install.sh"
    exit 1
fi

echo "→ Перезапуск бота и веб-API"
sudo -n "$SYSTEMCTL" restart fastboard-bot.service
sudo -n "$SYSTEMCTL" restart fastboard-web.service

echo "→ Проверка"
sleep 6
systemctl is-active --quiet gpu-ollama-tunnel.service \
    || { echo "!! Туннель к GPU не поднят"; systemctl status gpu-ollama-tunnel.service --no-pager -l | tail -20; exit 1; }
curl -fsS -m 15 http://127.0.0.1:11434/api/version >/dev/null \
    || { echo "!! Ollama на GPU-сервере недоступна через туннель"; exit 1; }
systemctl is-active --quiet fastboard-bot.service \
    || { echo "!! Бот не запустился"; journalctl -u fastboard-bot.service -n 40 --no-pager; exit 1; }
for _ in $(seq 1 20); do
    curl -fsS -m 5 http://127.0.0.1:8080/health >/dev/null 2>&1 && break
    sleep 3
done
curl -fsS -m 5 http://127.0.0.1:8080/health >/dev/null \
    || { echo "!! Веб-API Фиби не отвечает на /health"; journalctl -u fastboard-web.service -n 40 --no-pager; exit 1; }

echo "✓ Готово: бот и веб-API работают, модель доступна"
journalctl -u fastboard-bot.service -n 5 --no-pager
journalctl -u fastboard-web.service -n 5 --no-pager
