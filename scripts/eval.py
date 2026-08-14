#!/usr/bin/env python3
"""Контроль качества: проверки базы знаний и регрессия ответов консультанта.

Запускается после каждого обновления базы (scripts/daily_update.sh) и вручную.
Две независимые части:

* `--base`    — быстрые проверки самой базы, без обращения к модели: коллекции
                не опустели, кодировка цела, скриншоты распознаны, данные свежие.
* `--answers` — эталонные вопросы из evals/questions.json: ответ проверяется на
                ключевые термины, отсутствие служебных утечек и верную ссылку.

Отчёт пишется в state/eval-report.json, рядом с предыдущим — чтобы видеть
регрессии: что вчера отвечалось верно, а сегодня сломалось.

    python scripts/eval.py                 # база + ответы
    python scripts/eval.py --base          # только база (быстро, без GPU)
    python scripts/eval.py --answers --id knopka-ssylka
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUESTIONS_PATH = os.path.join(BASE_DIR, "evals", "questions.json")
STATE_DIR = os.path.join(BASE_DIR, "state")
REPORT_PATH = os.path.join(STATE_DIR, "eval-report.json")

# Служебные обороты, которых не должно быть ни в одном ответе: пользователь не
# видит ни фрагментов, ни контекста. Формулировки точные: просто «фрагмент» —
# нормальное слово, бот законно пишет «фрагмент JSON».
FORBIDDEN_PATTERNS = [
    r"фрагмент\w*\s*\d",          # «как видно из Фрагмента 3»
    r"в предоставленн\w+",
    r"в приведённ\w+ (фрагмент|контекст)\w*",
    r"в контексте (нет|отсутству)",
    r"<ссылка", r"<название",
]

# Признак сломанной кодировки: страницы, скачанные без учёта charset.
MOJIBAKE_MARKERS = ["Ð°", "Ñ€", "Ð¸Ð"]

MIN_EXPECTED = {"fastboard_docs": 300, "clickhouse_docs": 200, "widget_settings": 800}


def load_report():
    try:
        with open(REPORT_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def save_report(report):
    os.makedirs(STATE_DIR, exist_ok=True)
    tmp = REPORT_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    os.replace(tmp, REPORT_PATH)


def check_base():
    """Проверки базы знаний без обращения к модели."""
    import chromadb
    from rag_common import VECTORDB_DIR, OpenRouterEmbeddingFunction

    checks = []

    def add(name, ok, detail):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})
        print(f"  {'✅' if ok else '❌'} {name}: {detail}")

    print("\n=== База знаний ===")
    client = chromadb.PersistentClient(path=VECTORDB_DIR)
    ef = OpenRouterEmbeddingFunction()
    counts = {}
    for name, minimum in MIN_EXPECTED.items():
        try:
            counts[name] = client.get_collection(name, embedding_function=ef).count()
        except Exception as e:
            counts[name] = 0
            add(f"коллекция {name}", False, f"недоступна: {e}")
            continue
        add(f"коллекция {name}", counts[name] >= minimum,
            f"{counts[name]} фрагментов (минимум {minimum})")

    # Кодировка: одна битая страница означает, что скрапер снова читает ответ
    # как ISO-8859-1 и вся русская документация уходит в базу мусором.
    # Проверяем только страницы из манифеста — то, что реально попало в базу.
    try:
        with open(os.path.join(BASE_DIR, "scrape_manifest.json"), encoding="utf-8") as f:
            pages = json.load(f).get("pages", {})
    except (OSError, json.JSONDecodeError) as e:
        add("манифест", False, f"не читается: {e}")
        pages = {}

    broken, with_ocr, total = [], 0, 0
    for meta in pages.values():
        if meta.get("collection") != "fastboard_docs":
            continue
        path = os.path.join(BASE_DIR, meta.get("file", ""))
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except OSError:
            broken.append(os.path.basename(path) + " (нет файла)")
            continue
        total += 1
        if any(marker in text for marker in MOJIBAKE_MARKERS):
            broken.append(os.path.basename(path))
        if "Со скриншота" in text:
            with_ocr += 1
    add("кодировка страниц", not broken,
        "все страницы читаемы" if not broken else f"битых: {len(broken)} ({broken[:3]})")
    add("страниц в справке", total >= 140, f"{total} страниц")
    add("распознанные скриншоты", with_ocr >= 100, f"{with_ocr} страниц с текстом со скриншотов")

    # Сверка с манифестом: если страниц в базе меньше, чем обещает манифест,
    # значит прошлый прогон оборвался. Лог при этом выглядит здоровым
    # («обновлено 0, без изменений 251»), поэтому иначе поломку не заметить.
    try:
        with open(os.path.join(BASE_DIR, "scrape_manifest.json"), encoding="utf-8") as f:
            pages = json.load(f).get("pages", {})
        for collection_name in ("fastboard_docs", "clickhouse_docs"):
            promised = sum(1 for m in pages.values() if m.get("collection") == collection_name)
            col = client.get_or_create_collection(collection_name, embedding_function=ef)
            metas = col.get(include=["metadatas"]).get("metadatas") or []
            actual = len({m.get("url") for m in metas if m})
            add(f"полнота {collection_name}", actual >= promised,
                f"в базе {actual} страниц, в манифесте {promised}")
    except Exception as e:
        add("сверка с манифестом", False, f"не удалось выполнить: {e}")

    # Свежесть: манифест обновляется на каждом успешном прогоне индексатора.
    manifest_path = os.path.join(BASE_DIR, "scrape_manifest.json")
    try:
        with open(manifest_path, encoding="utf-8") as f:
            updated = json.load(f).get("updated")
        age_hours = (datetime.now(timezone.utc)
                     - datetime.fromisoformat(updated)).total_seconds() / 3600
        add("свежесть базы", age_hours < 48, f"обновлена {age_hours:.0f} ч назад")
    except Exception as e:
        add("свежесть базы", False, f"не удалось прочитать манифест: {e}")

    return checks, counts


def check_answers(only_id=None):
    """Эталонные вопросы: ответ должен содержать суть и верную ссылку."""
    import telegram_bot as bot

    with open(QUESTIONS_PATH, encoding="utf-8") as f:
        questions = json.load(f)
    if only_id:
        questions = [q for q in questions if q["id"] == only_id]

    print(f"\n=== Ответы: {len(questions)} эталонных вопросов ===")
    results = []
    for item in questions:
        started = time.time()
        try:
            # Тем же путём, что и живой бот: сначала готовые ответы про него
            # самого и про переход на человека, и только потом поиск по базе.
            answer = bot.canned_reply(item["question"]) or bot.rag.answer(item["question"])
            error = None
        except Exception as e:
            answer, error = "", f"{type(e).__name__}: {e}"
        elapsed = time.time() - started
        low = answer.lower()

        missing = [t for t in item.get("must_contain", []) if t.lower() not in low]
        forbidden = [t for t in item.get("must_not_contain", []) if t.lower() in low]
        forbidden += [p for p in FORBIDDEN_PATTERNS if re.search(p, low)]
        link = item.get("expect_link")
        link_ok = (link is None) or (link in answer)

        # Короткий ответ — не дефект: на «сто умножить на три» правильный
        # ответ это «300».
        ok = bool(not error and not missing and not forbidden and link_ok and answer.strip())
        results.append({
            "id": item["id"], "ok": ok, "seconds": round(elapsed, 1),
            "missing": missing, "forbidden": forbidden,
            "link_ok": link_ok, "error": error,
            "answer": answer[:1500],
        })

        flaws = []
        if error:
            flaws.append(f"ошибка: {error}")
        if missing:
            flaws.append(f"нет по сути: {missing}")
        if forbidden:
            flaws.append(f"лишнее: {forbidden}")
        if not link_ok:
            flaws.append("нет верной ссылки")
        print(f"  {'✅' if ok else '❌'} {item['id']} ({elapsed:.0f} с)"
              + (f" — {'; '.join(flaws)}" if flaws else ""))
    return results


def report_regressions(previous, results):
    """Что работало в прошлый раз и сломалось сейчас — самое важное в отчёте."""
    current_ids = {r["id"] for r in results}
    was_ok = {r["id"] for r in previous.get("answers", [])
              if r.get("ok") and r["id"] in current_ids}
    was_known = {r["id"] for r in previous.get("answers", []) if r["id"] in current_ids}
    now_ok = {r["id"] for r in results if r["ok"]}
    broke = sorted(was_ok - now_ok)
    fixed = sorted((now_ok - was_ok) & was_known)
    if broke:
        print(f"\n⚠️  РЕГРЕССИЯ: сломалось после обновления — {', '.join(broke)}")
    if fixed:
        print(f"✨ Починилось: {', '.join(fixed)}")
    return {"broke": broke, "fixed": fixed}


def show_last():
    """Печатает последний отчёт: приёмке не нужно занимать GPU, чтобы увидеть цифры."""
    report = load_report()
    if not report:
        print("Отчётов ещё нет — запустите python scripts/eval.py")
        return 1

    print(f"Проверка базы: {report.get('started', '?')}")
    for check in report.get("base", []):
        print(f"  {'✅' if check['ok'] else '❌'} {check['check']}: {check['detail']}")

    answers = report.get("answers", [])
    if answers:
        passed = sum(1 for a in answers if a["ok"])
        print(f"\nОтветы (прогон {report.get('answers_from', report.get('started', '?'))}): "
              f"{passed} из {len(answers)} ({passed / len(answers):.0%})")
        for a in answers:
            flaws = []
            if a.get("missing"):
                flaws.append(f"нет: {a['missing']}")
            if a.get("forbidden"):
                flaws.append(f"лишнее: {a['forbidden']}")
            if not a.get("link_ok", True):
                flaws.append("ссылка не та")
            if a.get("error"):
                flaws.append(a["error"][:60])
            print(f"  {'✅' if a['ok'] else '❌'} {a['id']} ({a.get('seconds', '?')} с)"
                  + (f" — {'; '.join(flaws)}" if flaws else ""))
    else:
        print("\nПолного прогона ответов ещё не было.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Контроль качества базы знаний и ответов.")
    parser.add_argument("--base", action="store_true", help="Только проверки базы (без модели).")
    parser.add_argument("--answers", action="store_true", help="Только эталонные вопросы.")
    parser.add_argument("--id", help="Прогнать один вопрос по идентификатору.")
    parser.add_argument("--show", action="store_true",
                        help="Показать результат последнего прогона, ничего не запуская.")
    parser.add_argument("--min-pass", type=float,
                        default=float(os.environ.get("EVAL_MIN_PASS", "0.8")),
                        help="Доля успешных ответов, ниже которой прогон считается упавшим.")
    args = parser.parse_args()
    if args.show:
        return show_last()

    run_base = args.base or not args.answers
    run_answers = args.answers or not args.base

    previous = load_report()
    report = {"started": datetime.now(timezone.utc).isoformat()}
    ok_overall = True

    # Быстрый прогон только по базе не должен стирать результат последнего
    # полного: иначе показать качество ответов можно, лишь заняв GPU на полчаса.
    if not run_answers and previous.get("answers"):
        report["answers"] = previous["answers"]
        report["pass_rate"] = previous.get("pass_rate")
        report["answers_from"] = previous.get("answers_started", previous.get("started"))

    if run_base:
        checks, counts = check_base()
        report["base"] = checks
        report["counts"] = counts
        ok_overall &= all(c["ok"] for c in checks)

    if run_answers:
        results = check_answers(args.id)
        if args.id:
            # Точечный прогон вливается в результаты последнего полного, а не
            # затирает их: иначе после проверки одного вопроса приёмке нечего
            # показать по всему набору.
            merged = {r["id"]: r for r in previous.get("answers", [])}
            merged.update({r["id"]: r for r in results})
            report["answers"] = list(merged.values())
            report["answers_started"] = previous.get("answers_started", report["started"])
        else:
            report["answers"] = results
            report["answers_started"] = report["started"]
        results = report["answers"]
        passed = sum(1 for r in results if r["ok"])
        share = passed / len(results) if results else 0
        report["pass_rate"] = round(share, 3)
        report["regressions"] = report_regressions(previous, results)
        print(f"\nОтветы: {passed} из {len(results)} ({share:.0%}), "
              f"порог {args.min_pass:.0%}")
        ok_overall &= share >= args.min_pass

    report["ok"] = ok_overall
    save_report(report)
    print(f"\n{'✅ Проверки пройдены' if ok_overall else '❌ Проверки не пройдены'}"
          f" — отчёт: {REPORT_PATH}")
    return 0 if ok_overall else 1


if __name__ == "__main__":
    sys.exit(main())
