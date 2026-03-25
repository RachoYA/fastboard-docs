#!/usr/bin/env python3
"""Scrape Fastboard and ClickHouse docs, save as markdown, index in ChromaDB."""

import os
import re
import time
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import chromadb
from chromadb.utils import embedding_functions

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
VECTORDB_DIR = os.path.join(BASE_DIR, "vectordb")

os.makedirs(os.path.join(DOCS_DIR, "fastboard"), exist_ok=True)
os.makedirs(os.path.join(DOCS_DIR, "clickhouse"), exist_ok=True)
os.makedirs(VECTORDB_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; FastboardDocsBot/1.0)"
}

def slugify(url):
    path = urlparse(url).path.strip("/").replace("/", "_")
    return re.sub(r"[^a-zA-Z0-9_\-]", "_", path) or "index"

def html_to_markdown(soup, base_url):
    """Extract main content and convert to simple markdown."""
    # Try common content selectors
    content = None
    for sel in ["article", "main", ".content", ".doc-content", "#content", "body"]:
        content = soup.select_one(sel)
        if content:
            break
    if not content:
        content = soup.body or soup

    # Remove nav, header, footer, scripts
    for tag in content.find_all(["nav", "header", "footer", "script", "style", "aside"]):
        tag.decompose()

    lines = []
    for elem in content.descendants:
        if not hasattr(elem, 'name'):
            continue
        if elem.name in ("h1", "h2", "h3", "h4"):
            level = int(elem.name[1])
            text = elem.get_text(strip=True)
            if text:
                lines.append(f"\n{'#' * level} {text}\n")
        elif elem.name == "p":
            text = elem.get_text(strip=True)
            if text:
                lines.append(text + "\n")
        elif elem.name == "li":
            text = elem.get_text(strip=True)
            if text:
                lines.append(f"- {text}")
        elif elem.name == "code" and elem.parent.name != "pre":
            pass  # inline code handled by parent text
        elif elem.name == "pre":
            code = elem.get_text()
            lines.append(f"\n```\n{code}\n```\n")

    return "\n".join(lines)

def scrape_site(start_url, save_dir, domain_filter, max_pages=200, delay=0.5):
    """Crawl a site recursively, save pages as markdown. Returns list of (url, filepath, text)."""
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
        title = soup.title.string.strip() if soup.title else url

        md = html_to_markdown(soup, url)
        md = f"# {title}\n\nSource: {url}\n\n{md}"

        slug = slugify(url)
        filepath = os.path.join(save_dir, f"{slug}.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)

        results.append((url, filepath, md))
        print(f"  [{len(visited)}] {url} → {slug}.md ({len(md)} chars)")

        # Collect links
        for a in soup.find_all("a", href=True):
            href = urljoin(url, a["href"]).split("#")[0]
            if domain_filter in href and href not in visited and href not in queue:
                queue.append(href)

        time.sleep(delay)

    return results

def chunk_text(text, chunk_size=800, overlap=100):
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def index_docs(results, collection):
    """Index scraped docs into ChromaDB."""
    total_chunks = 0
    for url, filepath, text in results:
        chunks = chunk_text(text)
        for j, chunk in enumerate(chunks):
            doc_id = hashlib.md5(f"{url}#{j}".encode()).hexdigest()
            collection.upsert(
                documents=[chunk],
                metadatas=[{"url": url, "chunk": j, "source": filepath}],
                ids=[doc_id]
            )
            total_chunks += 1
    return total_chunks

def main():
    print("=== Fastboard & ClickHouse Docs Indexer ===\n")

    # ChromaDB setup
    client = chromadb.PersistentClient(path=VECTORDB_DIR)
    ef = embedding_functions.DefaultEmbeddingFunction()

    # Delete existing collections to re-index fresh
    for name in ["fastboard_docs", "clickhouse_docs"]:
        try:
            client.delete_collection(name)
        except:
            pass

    fb_col = client.get_or_create_collection("fastboard_docs", embedding_function=ef)
    ch_col = client.get_or_create_collection("clickhouse_docs", embedding_function=ef)

    # --- Fastboard ---
    print("📄 Scraping Fastboard docs...")
    fb_results = scrape_site(
        start_url="https://help.fastboard.online/user/",
        save_dir=os.path.join(DOCS_DIR, "fastboard"),
        domain_filter="help.fastboard.online",
        max_pages=150,
        delay=0.3
    )
    print(f"\n✅ Fastboard: {len(fb_results)} страниц сохранено")

    print("\nИндексирую Fastboard в ChromaDB...")
    fb_chunks = index_docs(fb_results, fb_col)
    print(f"✅ Fastboard: {fb_chunks} чанков проиндексировано")

    # --- ClickHouse ---
    print("\n📄 Scraping ClickHouse docs (ru)...")
    ch_sections = [
        "https://clickhouse.com/docs/ru/sql-reference/data-types",
        "https://clickhouse.com/docs/ru/sql-reference/functions",
        "https://clickhouse.com/docs/ru/engines/table-engines",
        "https://clickhouse.com/docs/ru/sql-reference/statements",
        "https://clickhouse.com/docs/ru/getting-started",
    ]
    ch_results = []
    for section_url in ch_sections:
        print(f"  → {section_url}")
        res = scrape_site(
            start_url=section_url,
            save_dir=os.path.join(DOCS_DIR, "clickhouse"),
            domain_filter="clickhouse.com/docs/ru",
            max_pages=40,
            delay=0.3
        )
        ch_results.extend(res)
        # deduplicate
        seen = set()
        deduped = []
        for r in ch_results:
            if r[0] not in seen:
                seen.add(r[0])
                deduped.append(r)
        ch_results = deduped

    print(f"\n✅ ClickHouse: {len(ch_results)} страниц сохранено")

    print("\nИндексирую ClickHouse в ChromaDB...")
    ch_chunks = index_docs(ch_results, ch_col)
    print(f"✅ ClickHouse: {ch_chunks} чанков проиндексировано")

    # Summary
    print("\n" + "="*40)
    print("📊 ИТОГ:")
    print(f"  Fastboard: {len(fb_results)} страниц, {fb_chunks} чанков")
    print(f"  ClickHouse: {len(ch_results)} страниц, {ch_chunks} чанков")
    print(f"  ВСЕГО: {len(fb_results)+len(ch_results)} страниц, {fb_chunks+ch_chunks} чанков")
    print(f"  База данных: {VECTORDB_DIR}")
    print("="*40)

if __name__ == "__main__":
    main()
