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

from rag_common import (
    BASE_DIR,
    DOCS_DIR,
    VECTORDB_DIR,
    EMBEDDING_MODEL,
    OpenRouterEmbeddingFunction,
    get_chroma_client,
)

os.makedirs(os.path.join(DOCS_DIR, "fastboard"), exist_ok=True)
os.makedirs(os.path.join(DOCS_DIR, "clickhouse"), exist_ok=True)

MANIFEST_PATH = os.environ.get("MANIFEST_PATH", os.path.join(BASE_DIR, "scrape_manifest.json"))

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; FastboardDocsBot/1.0)"
}

# Теги, внутри которых ссылки/картинки рендерятся как инлайн (не дублируются).
INLINE_PARENTS = {"p", "li", "h1", "h2", "h3", "h4", "a", "figcaption", "td", "th"}

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


def crawl(start_url, domain_filter, max_pages=200, delay=0.5):
    """Обходит сайт рекурсивно. Возвращает список (url, markdown) без записи на диск."""
    visited = set()
    queue = [start_url]
    results = []

    session = requests.Session()
    session.headers.update(HEADERS)

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

        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else url

        md = html_to_markdown(soup, url)
        md = f"# {title}\n\nSource: {url}\n\n{md}"
        results.append((url, md))

        # Сбор ссылок для дальнейшего обхода
        for a in soup.find_all("a", href=True):
            href = urljoin(url, a["href"]).split("#")[0]
            if domain_filter in href and href not in visited and href not in queue:
                queue.append(href)

        time.sleep(delay)

    return results


def chunk_text(text, chunk_size=800, overlap=100):
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
    """Индексирует один документ: удаляет старые чанки этого URL и заливает новые."""
    try:
        collection.delete(where={"url": url})
    except Exception:
        pass
    chunks = chunk_text(text)
    ids, docs, metas = [], [], []
    rel = os.path.relpath(filepath, BASE_DIR)
    for j, chunk in enumerate(chunks):
        ids.append(hashlib.md5(f"{url}#{j}".encode()).hexdigest())
        docs.append(chunk)
        metas.append({"url": url, "chunk": j, "source": rel})
    if ids:
        collection.upsert(documents=docs, metadatas=metas, ids=ids)
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
    args = parser.parse_args()

    print("=== Fastboard & ClickHouse Docs Indexer ===")
    print(f"🔌 Эмбеддинги через OpenRouter: {EMBEDDING_MODEL}")
    print(f"⚙️  Режим: {'ПОЛНАЯ ПЕРЕСБОРКА' if args.full else 'инкрементальный'}\n")

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

    client = get_chroma_client()
    ef = OpenRouterEmbeddingFunction()

    if full:
        for name in ["fastboard_docs", "clickhouse_docs"]:
            try:
                client.delete_collection(name)
            except Exception:
                pass

    fb_col = client.get_or_create_collection("fastboard_docs", embedding_function=ef)
    ch_col = client.get_or_create_collection("clickhouse_docs", embedding_function=ef)

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
        domain_filter="help.fastboard.online",
        max_pages=150,
        delay=0.3,
    )
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

    save_manifest(manifest)

    # Итог
    print("\n" + "=" * 44)
    print("📊 ИТОГ (дельта за запуск):")
    print(f"  Обновлено страниц: {fb_stats['changed'] + ch_stats['changed']}")
    print(f"  Без изменений:     {fb_stats['skipped'] + ch_stats['skipped']}")
    print(f"  Удалено:           {fb_stats['removed'] + ch_stats['removed']}")
    print(f"  Переиндексировано чанков: {fb_stats['chunks'] + ch_stats['chunks']}")
    print(f"  Манифест: {MANIFEST_PATH}")
    print(f"  База данных: {VECTORDB_DIR}")
    print("=" * 44)


if __name__ == "__main__":
    main()
