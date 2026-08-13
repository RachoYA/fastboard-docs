#!/usr/bin/env python3
"""Самопроверка консультанта: канал до модели, эмбеддинги, поиск, ответ, распознавание.

Генерирует тестовый «скриншот» с русским текстом, SQL и числами, прогоняет его
через vision-модель и проверяет, что текст с картинки прочитан.

    ./.venv/bin/python scripts/selfcheck.py
"""

import io
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests

import telegram_bot as bot
from rag_common import CHAT_MODEL, EMBEDDING_MODEL, OpenRouterEmbeddingFunction

FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
]

# Что должно быть прочитано с тестовой картинки
MARKERS = ["user_id", "47", "1 248", "Выручка", "SELECT"]

ok_all = True


def step(name):
    print(f"\n=== {name} ===")


def verdict(cond, good, bad):
    global ok_all
    print(("  ✅ " + good) if cond else ("  ❌ " + bad))
    ok_all = ok_all and bool(cond)
    return cond


def find_font():
    for path in FONTS:
        if os.path.exists(path):
            return path
    return None


def make_test_image():
    """Рисует «скриншот» Fastboard с ошибкой, SQL и числами."""
    import pymupdf

    font = find_font()
    doc = pymupdf.open()
    page = doc.new_page(width=900, height=560)
    fn = "F0"
    put = lambda pos, text, size=15, color=(0.1, 0.1, 0.12): page.insert_text(
        pos, text, fontsize=size, color=color,
        **({"fontfile": font, "fontname": fn} if font else {"fontname": "helv"}))

    page.draw_rect(pymupdf.Rect(0, 0, 900, 60), color=None, fill=(0.13, 0.17, 0.26))
    put((28, 38), "Fastboard — Диспетчер данных", 20, (1, 1, 1))

    page.draw_rect(pymupdf.Rect(28, 90, 872, 160), color=(0.85, 0.2, 0.2), fill=(0.99, 0.93, 0.93))
    put((44, 118), "Ошибка выполнения запроса", 16, (0.7, 0.1, 0.1))
    put((44, 144), "Code: 47. DB::Exception: Missing columns: 'user_id'", 13, (0.5, 0.1, 0.1))

    put((28, 200), "SQL-редактор:", 14)
    page.draw_rect(pymupdf.Rect(28, 214, 872, 260), color=(0.8, 0.8, 0.85), fill=(0.96, 0.96, 0.98))
    put((44, 242), "SELECT count() FROM events WHERE user_id = 42", 13, (0.15, 0.25, 0.5))

    put((28, 300), "Показатели за месяц:", 14)
    put((44, 330), "Заказы: 1 248", 14)
    put((44, 356), "Выручка: 3 750 000 руб.", 14)

    put((520, 300), "Продажи по неделям", 13)
    for i, h in enumerate([40, 70, 55, 95]):
        x = 540 + i * 60
        page.draw_rect(pymupdf.Rect(x, 400 - h, x + 40, 400), color=None, fill=(0.2, 0.45, 0.8))
    png = page.get_pixmap(dpi=110).tobytes("png")
    doc.close()
    return png


def main():
    print(f"Чат-модель: {CHAT_MODEL}\nЭмбеддинги: {EMBEDDING_MODEL}\nOllama: {bot.OLLAMA_URL}")

    step("1. Канал до GPU-сервера")
    try:
        tags = requests.get(f"{bot.OLLAMA_URL}/api/tags", timeout=15).json()
        names = [m["name"] for m in tags.get("models", [])]
        print("  модели:", ", ".join(names))
        verdict(CHAT_MODEL in names, f"{CHAT_MODEL} доступна", f"{CHAT_MODEL} не найдена")
        verdict(any(n.startswith(EMBEDDING_MODEL) for n in names),
                f"{EMBEDDING_MODEL} доступна", f"{EMBEDDING_MODEL} не найдена")
    except Exception as e:
        verdict(False, "", f"туннель до Ollama не работает: {e}")
        return 1

    step("2. Эмбеддинги")
    t = time.time()
    vec = OpenRouterEmbeddingFunction()(["Как создать дашборд в Fastboard?"])
    verdict(vec and len(vec[0]) > 100, f"вектор {len(vec[0])} измерений за {time.time() - t:.1f} с", "эмбеддинги не считаются")

    step("3. База знаний")
    total = 0
    for col in bot.rag.collections():
        n = col.count()
        total += n
        print(f"  {col.name}: {n} фрагментов")
    verdict(total > 0, f"всего {total} фрагментов", "база знаний пуста — запустите scrape_and_index.py")

    step("4. Ответ по документации (текст)")
    t = time.time()
    answer = bot.rag.answer("Как создать дашборд в Fastboard?")
    print("  " + answer[:400].replace("\n", "\n  "))
    verdict(len(answer) > 80, f"ответ получен за {time.time() - t:.1f} с", "модель вернула пустой ответ")

    step("5. Распознавание изображения (картинка + текст на ней)")
    png = make_test_image()
    open("/tmp/selfcheck_screenshot.png", "wb").write(png)
    print(f"  тестовый скриншот: /tmp/selfcheck_screenshot.png ({len(png)} Б)")
    t = time.time()
    recognized = bot.describe_image(png, "что за ошибка на скриншоте?")
    print("  --- распознано ---")
    print("  " + recognized[:900].replace("\n", "\n  "))
    print(f"  --- за {time.time() - t:.1f} с ---")

    norm = recognized.lower().replace(" ", " ")
    found = [m for m in MARKERS if m.lower().replace(" ", "") in norm.replace(" ", "")]
    print(f"  найдены маркеры: {found} из {MARKERS}")
    verdict(len(found) >= 4, "текст с изображения прочитан", "текст с изображения прочитан плохо")

    step("6. Ответ по картинке с учётом документации")
    t = time.time()
    reply = bot.rag.answer("Что за ошибка на скриншоте и как её исправить?", extra_context=recognized)
    print("  " + reply[:500].replace("\n", "\n  "))
    verdict(len(reply) > 80, f"ответ получен за {time.time() - t:.1f} с", "пустой ответ")

    print("\n" + ("✅ Все проверки пройдены" if ok_all else "❌ Есть проблемы, см. выше"))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
