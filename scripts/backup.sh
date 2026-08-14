#!/usr/bin/env bash
# Резервная копия того, что нельзя восстановить из git:
#   .env                       — токен бота и настройки
#   vectordb/                  — векторная база (переиндексация занимает ~40 минут)
#   state/image_ocr_cache.json — распознанные скриншоты документации (~800 картинок,
#                                это часы работы GPU)
#   scrape_manifest.json       — состояние инкрементального обхода
#
# Запускается таймером раз в сутки. Хранит последние BACKUP_KEEP копий.
# BACKUP_DIR по умолчанию локальный: это спасает от порчи данных, но не от
# потери сервера — для этого задайте каталог на смонтированном удалённом диске
# либо настройте отправку архива на второй хост.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

BACKUP_DIR="${BACKUP_DIR:-$HOME/backups/fastboard-docs}"
BACKUP_KEEP="${BACKUP_KEEP:-7}"
mkdir -p "$BACKUP_DIR"

stamp=$(date -u +%Y%m%d-%H%M)
archive="$BACKUP_DIR/fastboard-docs-$stamp.tar.gz"

tar czf "$archive" \
    --warning=no-file-changed \
    .env vectordb state scrape_manifest.json 2>/dev/null \
    || true   # tar ругается, если база менялась во время архивации — это не ошибка

if [ ! -s "$archive" ]; then
    echo "!! Архив пустой — резервная копия не создана" >&2
    exit 1
fi

size=$(du -h "$archive" | cut -f1)
echo "$(date -u +%FT%TZ) резервная копия: $archive ($size)"

# Чистим старые, оставляя последние BACKUP_KEEP
ls -1t "$BACKUP_DIR"/fastboard-docs-*.tar.gz 2>/dev/null \
    | tail -n +$((BACKUP_KEEP + 1)) \
    | xargs -r rm -f

echo "Копий в $BACKUP_DIR: $(ls -1 "$BACKUP_DIR"/fastboard-docs-*.tar.gz 2>/dev/null | wc -l)"
