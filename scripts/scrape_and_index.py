#!/usr/bin/env python3
"""Скрапер документации Fastboard и ClickHouse.

Сохраняет страницы в Markdown (с ссылками и картинками) и индексирует их в
ChromaDB на эмбеддингах OpenRouter.

Режим по умолчанию — инкрементальный: обновляются и переиндексируются только
изменившиеся страницы (сравнение по хэшу содержимого, состояние хранится в
scrape_manifest.json). Это позволяет запускать скрипт ежедневно и получать
только «дельту».

    python scripts/scrape_and_index.py            # инкрементальное обновление
    python scripts/scrape_and_index.py --full     # полная пересборка с нуля
    python scripts/scrape_and_index.py --prune     # удалять исчезнувшие страницы
"""

import os
import re
import json
import time
import argparse
import hashlib
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

import chromadb
from rag_common import (
    BASE_DIR,
    DOCS_DIR,
    VECTORDB_DIR,
    EMBEDDING_MODEL,
    OpenRouterEmbeddingFunction,
)

os.makedirs(os.path.join(DOCS_DIR, "fastboard"), exist_ok=True)
os.makedirs(os.path.join(DOCS_DIR, "clickhouse"), exist_ok=True)
os.makedirs(VECTORDB_DIR, exist_ok=True)

MANIFEST_PATH = os.path.join(BASE_DIR, "scrape_manifest.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; FastboardDocsBot/1.0)"
}

# Теги, внутри которых ссылки/картинки рендерятся как инлайн (не дублируются).
INLINE_PARENTS = {"p", "li", "h1", "h2", "h3", "h4", "a", "figcaption", "td", "th"}

# Минимум слов на странице, чтобы её индексировать (отсекает заглушки и редиректы)
MIN_WORDS = 40

# Распознавание скриншотов документации. В справке Fastboard значительная часть
# инструкций показана только на картинках, поэтому текст с них вытаскивается
# vision-моделью и попадает в Markdown (и в поиск) рядом со ссылкой на скриншот.
OCR_IMAGES = os.environ.get("OCR_IMAGES", "1") == "1"
OCR_CACHE_PATH = os.path.join(BASE_DIR, "state", "image_ocr_cache.json")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\((https?://[^)\s]+)\)")
OCR_SKIP_EXT = (".svg", ".gif")

# Справочник настроек виджетов (docs/reference) — своя коллекция: это плотная
# таблица свойств, и в общей выдаче она забивала бы обычные статьи справки.
REFERENCE_DIR = os.path.join(DOCS_DIR, "reference")
REFERENCE_COLLECTION = "widget_settings"
REFERENCE_CHUNK_ROWS = 12

# Блочные теги: их рендерит основной цикл по descendants. render_inline НЕ должен
# рекурсивно входить в них, иначе вложенные блоки (напр. <ul> внутри <li> или <p>)
# попадут в вывод дважды.
BLOCK_TAGS = {
    "p", "div", "section", "article", "ul", "ol", "li", "pre", "table",
    "thead", "tbody", "tr", "td", "th", "blockquote", "figure", "dl",
    "h1", "h2", "h3", "h4", "h5", "h6",
}


def slugify(url):
    path = urlparse(url).path.strip("/").replace("/", "_")
    return re.sub(r"[^a-zA-Z0-9_\-]", "_", path) or "index"


def _norm_href(href, base_url):
    """Абсолютизирует ссылку, сохраняя якоря."""
    if not href:
        return None
    if href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
        return href
    return urljoin(base_url, href)


def _img_src(tag, base_url):
    """Извлекает адрес картинки, учитывая ленивую загрузку и srcset."""
    raw = (
        tag.get("src")
        or tag.get("data-src")
        or tag.get("data-original")
        or tag.get("data-lazy-src")
    )
    if not raw:
        srcset = tag.get("srcset") or tag.get("data-srcset")
        if srcset:
            # первый кандидат из srcset: "url 1x, url2 2x"
            raw = srcset.split(",")[0].strip().split(" ")[0]
    return _norm_href(raw, base_url)


def render_inline(elem, base_url, descend_blocks=False):
    """Преобразует инлайн-содержимое элемента в Markdown с ссылками и картинками.

    descend_blocks=True — рекурсивно входить и в блочные теги (нужно для ячеек
    таблиц, где содержимое часто завёрнуто в <p>/<div>). По умолчанию блоки
    пропускаются: их рендерит основной цикл по descendants (иначе будет дубль).
    """
    parts = []
    for child in elem.children:
        name = getattr(child, "name", None)
        if name is None:
            parts.append(str(child))
        elif name == "a":
            text = render_inline(child, base_url, descend_blocks) or child.get_text(strip=True)
            href = _norm_href(child.get("href"), base_url)
            if href and text:
                parts.append(f"[{text}]({href})")
            elif href:
                parts.append(f"<{href}>")
            else:
                parts.append(text)
        elif name == "img":
            src = _img_src(child, base_url)
            if src:
                parts.append(f"![{child.get('alt', '')}]({src})")
        elif name == "code":
            parts.append(f"`{child.get_text()}`")
        elif name in ("strong", "b"):
            parts.append(f"**{render_inline(child, base_url, descend_blocks)}**")
        elif name in ("em", "i"):
            parts.append(f"*{render_inline(child, base_url, descend_blocks)}*")
        elif name == "br":
            parts.append(" ")
        elif name in BLOCK_TAGS:
            if descend_blocks:
                parts.append(" " + render_inline(child, base_url, True) + " ")
            else:
                # вложенный блок обработает основной цикл — пропускаем, чтобы не дублировать
                continue
        else:
            parts.append(render_inline(child, base_url, descend_blocks))
    return re.sub(r"\s+", " ", "".join(parts)).strip()


def render_table(table, base_url):
    """Преобразует <table> в Markdown-таблицу (с экранированием '|')."""
    rows = []
    for tr in table.find_all("tr"):
        cells = tr.find_all(["th", "td"], recursive=False) or tr.find_all(["th", "td"])
        if not cells:
            continue
        rows.append([render_inline(c, base_url, descend_blocks=True).replace("|", "\\|")
                     for c in cells])
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    header = rows[0]
    out = ["| " + " | ".join(header) + " |",
           "| " + " | ".join(["---"] * width) + " |"]
    for r in rows[1:]:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


def html_to_markdown(soup, base_url):
    """Извлекает основной контент и конвертирует в Markdown (с ссылками и картинками)."""
    content = None
    for sel in ["article", "main", ".content", ".doc-content", "#content", "body"]:
        content = soup.select_one(sel)
        if content:
            break
    if not content:
        content = soup.body or soup

    # Удаляем навигацию, шапку, подвал, скрипты
    for tag in content.find_all(["nav", "header", "footer", "script", "style", "aside"]):
        tag.decompose()

    lines = []
    for elem in content.descendants:
        if not hasattr(elem, "name") or elem.name is None:
            continue
        # <table>/<pre> рендерятся целиком — их потомков пропускаем, чтобы не дублировать
        if elem.find_parent(["table", "pre"]) is not None:
            continue
        if elem.name in ("h1", "h2", "h3", "h4"):
            level = int(elem.name[1])
            text = render_inline(elem, base_url)
            if text:
                lines.append(f"\n{'#' * level} {text}\n")
        elif elem.name == "p":
            text = render_inline(elem, base_url)
            if text:
                lines.append(text + "\n")
        elif elem.name == "li":
            text = render_inline(elem, base_url)
            if text:
                lines.append(f"- {text}")
        elif elem.name == "pre":
            code = elem.get_text()
            lines.append(f"\n```\n{code}\n```\n")
        elif elem.name == "table":
            md_table = render_table(elem, base_url)
            if md_table:
                lines.append("\n" + md_table + "\n")
        elif elem.name == "img":
            # Картинки, не вложенные в обрабатываемые инлайн-блоки — отдельной строкой
            parent_name = elem.parent.name if elem.parent is not None else None
            if parent_name in INLINE_PARENTS:
                continue
            src = _img_src(elem, base_url)
            if src:
                lines.append(f"\n![{elem.get('alt', '')}]({src})\n")

    return "\n".join(lines)


def load_ocr_cache():
    """Кэш распознанных скриншотов: ссылка на картинку → текст с неё."""
    try:
        with open(OCR_CACHE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def save_ocr_cache(cache):
    os.makedirs(os.path.dirname(OCR_CACHE_PATH), exist_ok=True)
    tmp = OCR_CACHE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=1)
    os.replace(tmp, OCR_CACHE_PATH)


def annotate_images(md, session, cache, stats):
    """Дописывает под каждым скриншотом распознанный с него текст.

    Ссылка на сам скриншот сохраняется, поэтому в ответе консультанта можно
    сослаться на конкретную картинку из документации.
    """
    import vision

    def replace(match):
        src = match.group(1)
        if src.lower().endswith(OCR_SKIP_EXT):
            return match.group(0)

        text = cache.get(src)
        if text is None:
            try:
                resp = session.get(src, timeout=30)
                resp.raise_for_status()
                text = vision.ocr_image(resp.content).strip()
                stats["ocr_new"] += 1
                print(f"    👁 {src.rsplit('/', 1)[-1]}: {len(text)} симв.")
            except Exception as e:
                print(f"    ⚠️  не удалось распознать {src}: {e}")
                text = ""
            cache[src] = text
            if stats["ocr_new"] % 5 == 0:
                save_ocr_cache(cache)
        else:
            stats["ocr_cached"] += 1

        if not text or text.lower().startswith("нет текста"):
            return match.group(0)
        body = "\n".join("> " + line for line in text.splitlines() if line.strip())
        return f"{match.group(0)}\n\n> **Со скриншота** ([изображение]({src})):\n{body}\n"

    return IMAGE_RE.sub(replace, md)


def crawl(start_url, domain_filter, max_pages=200, delay=0.5, ocr=False, ocr_stats=None):
    """Обходит сайт рекурсивно. Возвращает список (url, markdown) без записи на диск."""
    visited = set()
    queue = [start_url]
    results = []

    session = requests.Session()
    session.headers.update(HEADERS)

    ocr_cache = load_ocr_cache() if ocr else {}
    if ocr_stats is None:
        ocr_stats = {"ocr_new": 0, "ocr_cached": 0}

    while queue and len(visited) < max_pages:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)

        try:
            resp = session.get(url, timeout=15)
            if resp.status_code != 200:
                print(f"  SKIP {url} ({resp.status_code})")
                continue
            if "text/html" not in resp.headers.get("content-type", ""):
                continue
        except Exception as e:
            print(f"  ERROR {url}: {e}")
            continue

        # ВАЖНО: разбираем resp.content, а не resp.text. Если сервер не указал
        # charset (так отдаёт help.fastboard.online), requests декодирует ответ
        # как ISO-8859-1 и вся кириллица превращается в «Ð Ð°Ð±Ð¾ÑÐ°». BeautifulSoup
        # же определяет кодировку по <meta charset> и разбирает страницу верно.
        soup = BeautifulSoup(resp.content, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else url

        body = html_to_markdown(soup, url)
        # Пустые страницы (редиректы, заглушки) только засоряют поиск: по ним
        # находятся «источники» без единого факта.
        if len(body.split()) < MIN_WORDS:
            print(f"  SKIP {url} (пустая страница)")
        else:
            if ocr:
                body = annotate_images(body, session, ocr_cache, ocr_stats)
            results.append((url, f"# {title}\n\nSource: {url}\n\n{body}"))

        # Сбор ссылок для дальнейшего обхода
        for a in soup.find_all("a", href=True):
            href = urljoin(url, a["href"]).split("#")[0]
            if domain_filter in href and href not in visited and href not in queue:
                queue.append(href)

        time.sleep(delay)

    if ocr:
        save_ocr_cache(ocr_cache)
    return results


def chunk_text(text, chunk_size=300, overlap=60):
    """Разбивает текст на перекрывающиеся чанки."""
    words = text.split()
    step = max(1, chunk_size - overlap)  # защита от бесконечного цикла при overlap >= chunk_size
    chunks = []
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i:i + chunk_size]))
        i += step
    return chunks


def index_one(url, filepath, text, collection):
    """Переиндексирует один документ.

    Сначала перезаписываются чанки, и только потом удаляются лишние: если
    удалять сначала, страница на время индексации выпадает из поиска и бот
    отвечает «этого нет в базе знаний» на вопрос, ответ на который есть.
    """
    chunks = chunk_text(text)
    # Название статьи повторяется в каждом фрагменте: без него середина страницы
    # теряет тему («Вкладка Доступ»), и вопрос своими словами её не находит.
    first_line = text.lstrip().splitlines()[0] if text.strip() else ""
    title = first_line.lstrip("# ").split("|")[0].strip()
    ids, docs, metas = [], [], []
    rel = os.path.relpath(filepath, BASE_DIR)
    for j, chunk in enumerate(chunks):
        ids.append(hashlib.md5(f"{url}#{j}".encode()).hexdigest())
        docs.append(f"{title}\n{chunk}" if title else chunk)
        metas.append({"url": url, "chunk": j, "source": rel})
    if ids:
        collection.upsert(documents=docs, metadatas=metas, ids=ids)

    # Хвост от прошлой версии страницы (если раньше чанков было больше)
    try:
        collection.delete(where={"$and": [{"url": url}, {"chunk": {"$gte": len(ids)}}]})
    except Exception:
        pass
    return len(ids)


def sync_collection(crawled, save_dir, collection, manifest, force=False, prune=False):
    """Синхронизирует результаты обхода с диском, ChromaDB и манифестом.

    Возвращает статистику: changed, skipped, removed, chunks.
    """
    pages = manifest.setdefault("pages", {})
    col_name = collection.name
    stats = {"changed": 0, "skipped": 0, "removed": 0, "chunks": 0}
    seen = set()

    for url, md in crawled:
        seen.add(url)
        slug = slugify(url)
        filepath = os.path.join(save_dir, f"{slug}.md")
        h = hashlib.sha256(md.encode("utf-8")).hexdigest()
        prev = pages.get(url)

        if (not force) and prev and prev.get("hash") == h and os.path.exists(filepath):
            stats["skipped"] += 1
            continue

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)
        stats["chunks"] += index_one(url, filepath, md, collection)
        pages[url] = {
            "hash": h,
            "file": os.path.relpath(filepath, BASE_DIR),
            "collection": col_name,
        }
        stats["changed"] += 1
        print(f"  ~ {url} → {slug}.md (обновлено)")

    # Удаление исчезнувших страниц этой коллекции (только при --prune)
    if prune:
        for url in [u for u, m in pages.items()
                    if m.get("collection") == col_name and u not in seen]:
            try:
                collection.delete(where={"url": url})
            except Exception:
                pass
            old_file = os.path.join(BASE_DIR, pages[url].get("file", ""))
            if old_file and os.path.exists(old_file):
                os.remove(old_file)
            del pages[url]
            stats["removed"] += 1
            print(f"  - {url} (удалено)")

    return stats


def chunk_reference(md, title):
    """Режет справочник по строкам таблицы, повторяя заголовок в каждом куске.

    Обычная нарезка по словам рвёт таблицу так, что кусок теряет и виджет,
    и раздел настроек — и найти по нему потом ничего нельзя.
    """
    rows = [line for line in md.splitlines() if line.startswith("| ") and not set(line) <= set("|- ")]
    chunks = []
    for i in range(0, len(rows), REFERENCE_CHUNK_ROWS):
        chunks.append(f"{title}\n" + "\n".join(rows[i:i + REFERENCE_CHUNK_ROWS]))
    return chunks or [md]


def sync_reference(collection, manifest, force=False):
    """Индексирует docs/reference/*.md — справочник свойств виджетов."""
    stats = {"changed": 0, "skipped": 0, "chunks": 0}
    if not os.path.isdir(REFERENCE_DIR):
        return stats

    pages = manifest.setdefault("pages", {})
    for name in sorted(os.listdir(REFERENCE_DIR)):
        if not name.endswith(".md") or name == "README.md":
            continue
        filepath = os.path.join(REFERENCE_DIR, name)
        with open(filepath, encoding="utf-8") as f:
            md = f.read()
        key = f"reference://{name}"
        h = hashlib.sha256(md.encode("utf-8")).hexdigest()
        if (not force) and pages.get(key, {}).get("hash") == h:
            stats["skipped"] += 1
            continue

        title = md.splitlines()[0].lstrip("# ").strip()
        chunks = chunk_reference(md, title)
        ids = [hashlib.md5(f"{key}#{j}".encode()).hexdigest() for j in range(len(chunks))]
        metas = [{"url": title, "chunk": j, "source": os.path.relpath(filepath, BASE_DIR)}
                 for j in range(len(chunks))]
        for i in range(0, len(chunks), 256):
            collection.upsert(documents=chunks[i:i + 256], metadatas=metas[i:i + 256],
                              ids=ids[i:i + 256])
        try:
            collection.delete(where={"$and": [{"url": title}, {"chunk": {"$gte": len(chunks)}}]})
        except Exception:
            pass

        pages[key] = {"hash": h, "file": os.path.relpath(filepath, BASE_DIR),
                      "collection": collection.name}
        stats["changed"] += 1
        stats["chunks"] += len(chunks)
        print(f"  ~ {name} → {len(chunks)} фрагментов")
    return stats


def load_manifest():
    if os.path.exists(MANIFEST_PATH):
        try:
            with open(MANIFEST_PATH, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"version": 1, "updated": None, "pages": {}}


def save_manifest(manifest):
    manifest["updated"] = datetime.now(timezone.utc).isoformat()
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2, sort_keys=True)


def main():
    parser = argparse.ArgumentParser(description="Скрапер и индексатор документации (инкрементальный).")
    parser.add_argument("--full", action="store_true", help="Полная пересборка: очистить коллекции и переиндексировать всё.")
    parser.add_argument("--prune", action="store_true", help="Удалять страницы, исчезнувшие с источника.")
    parser.add_argument("--no-ocr", action="store_true",
                        help="Не распознавать текст на скриншотах документации.")
    args = parser.parse_args()
    ocr = OCR_IMAGES and not args.no_ocr
    ocr_stats = {"ocr_new": 0, "ocr_cached": 0}

    print("=== Fastboard & ClickHouse Docs Indexer ===")
    print(f"🔌 Эмбеддинги через OpenRouter: {EMBEDDING_MODEL}")
    print(f"⚙️  Режим: {'ПОЛНАЯ ПЕРЕСБОРКА' if args.full else 'инкрементальный'}")
    print(f"👁  Распознавание скриншотов: {'включено' if ocr else 'выключено'}\n")

    manifest = {"version": 1, "updated": None, "pages": {}} if args.full else load_manifest()

    # Смена модели эмбеддингов делает старые векторы несовместимыми (другая
    # размерность) — в этом случае нужна полная пересборка.
    prev_model = manifest.get("embedding_model")
    model_changed = prev_model is not None and prev_model != EMBEDDING_MODEL
    full = args.full or model_changed
    if model_changed:
        print(f"⚠️  Модель эмбеддингов изменилась ({prev_model} → {EMBEDDING_MODEL}). "
              f"Выполняю полную пересборку.\n")
        manifest = {"version": 1, "updated": None, "pages": {}}
    manifest["embedding_model"] = EMBEDDING_MODEL

    client = chromadb.PersistentClient(path=VECTORDB_DIR)
    ef = OpenRouterEmbeddingFunction()

    # Коллекции чистятся не здесь, а после обхода: обход — самая долгая часть,
    # и если процесс прервётся, база знаний не должна остаться пустой.
    def reset_collections():
        if not full:
            return
        for name in ["fastboard_docs", "clickhouse_docs", REFERENCE_COLLECTION]:
            try:
                client.delete_collection(name)
            except Exception:
                pass

    fb_col = client.get_or_create_collection("fastboard_docs", embedding_function=ef)
    ch_col = client.get_or_create_collection("clickhouse_docs", embedding_function=ef)
    ref_col = client.get_or_create_collection(REFERENCE_COLLECTION, embedding_function=ef)

    # Если база пуста (например, потерян том vectordb) — форсируем полную
    # индексацию, даже в инкрементальном режиме, чтобы не остаться с пустым индексом.
    fb_force = full or fb_col.count() == 0
    ch_force = full or ch_col.count() == 0
    if (fb_force or ch_force) and not args.full:
        print("ℹ️  Обнаружена пустая/несовместимая база — будет переиндексировано всё "
              "(возможен повышенный расход эмбеддингов).\n")

    # --- Fastboard ---
    print("📄 Обход Fastboard...")
    fb_crawled = crawl(
        start_url="https://help.fastboard.online/user/",
        # Только /user/: раздел /gostech/ — почти дословный дубликат для ГосТеха,
        # он съедал лимит страниц и подмешивался в выдачу вместо основной справки.
        domain_filter="help.fastboard.online/user/",
        max_pages=400,
        delay=0.3,
        ocr=ocr,
        ocr_stats=ocr_stats,
    )
    reset_collections()
    fb_col = client.get_or_create_collection("fastboard_docs", embedding_function=ef)
    ch_col = client.get_or_create_collection("clickhouse_docs", embedding_function=ef)
    ref_col = client.get_or_create_collection(REFERENCE_COLLECTION, embedding_function=ef)
    fb_stats = sync_collection(
        fb_crawled, os.path.join(DOCS_DIR, "fastboard"), fb_col, manifest,
        force=fb_force, prune=args.prune,
    )
    print(f"✅ Fastboard: обход {len(fb_crawled)}, обновлено {fb_stats['changed']}, "
          f"без изменений {fb_stats['skipped']}, удалено {fb_stats['removed']}")
    save_manifest(manifest)  # durability: фиксируем прогресс до обхода ClickHouse

    # --- ClickHouse ---
    print("\n📄 Обход ClickHouse (ru)...")
    ch_sections = [
        "https://clickhouse.com/docs/ru/sql-reference/data-types",
        "https://clickhouse.com/docs/ru/sql-reference/functions",
        "https://clickhouse.com/docs/ru/engines/table-engines",
        "https://clickhouse.com/docs/ru/sql-reference/statements",
        "https://clickhouse.com/docs/ru/getting-started",
    ]
    ch_crawled = []
    seen = set()
    for section_url in ch_sections:
        print(f"  → {section_url}")
        for url, md in crawl(section_url, "clickhouse.com/docs/ru", max_pages=40, delay=0.3):
            if url not in seen:
                seen.add(url)
                ch_crawled.append((url, md))
    ch_stats = sync_collection(
        ch_crawled, os.path.join(DOCS_DIR, "clickhouse"), ch_col, manifest,
        force=ch_force, prune=args.prune,
    )
    print(f"✅ ClickHouse: обход {len(ch_crawled)}, обновлено {ch_stats['changed']}, "
          f"без изменений {ch_stats['skipped']}, удалено {ch_stats['removed']}")

    # --- Справочник настроек виджетов ---
    print("\n📐 Справочник настроек виджетов (docs/reference)...")
    ref_stats = sync_reference(ref_col, manifest, force=full or ref_col.count() == 0)
    print(f"✅ Справочник: обновлено файлов {ref_stats['changed']}, "
          f"без изменений {ref_stats['skipped']}")

    save_manifest(manifest)

    # Итог
    print("\n" + "=" * 44)
    print("📊 ИТОГ (дельта за запуск):")
    print(f"  Обновлено страниц: {fb_stats['changed'] + ch_stats['changed']}")
    print(f"  Без изменений:     {fb_stats['skipped'] + ch_stats['skipped']}")
    print(f"  Удалено:           {fb_stats['removed'] + ch_stats['removed']}")
    print(f"  Переиндексировано чанков: {fb_stats['chunks'] + ch_stats['chunks'] + ref_stats['chunks']}")
    print(f"  Распознано скриншотов: {ocr_stats['ocr_new']} новых, {ocr_stats['ocr_cached']} из кэша")
    print(f"  Манифест: {MANIFEST_PATH}")
    print(f"  База данных: {VECTORDB_DIR}")
    print("=" * 44)


if __name__ == "__main__":
    main()
