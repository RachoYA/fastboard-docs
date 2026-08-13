#!/usr/bin/env python3
"""Раскладывает выгрузку настроек виджетов по файлам справочника.

На вход — большой WIDGET-SETTINGS-TABLE.md (таблица свойств всех виджетов,
собранная по реальным проектам). На выходе — по файлу на тип виджета в
docs/reference/, которые индексатор кладёт в отдельную коллекцию.

    python scripts/import_widget_settings.py ~/Downloads/WIDGET-SETTINGS-TABLE.md
"""

import argparse
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFERENCE_DIR = os.path.join(BASE_DIR, "docs", "reference")

SECTION_RE = re.compile(r"^## (.+?) \(`([a-zA-Z]+)`\)\s*$")


def split_sections(text):
    """Возвращает [(человекочитаемое имя, тип, строки раздела)] и шапку файла."""
    lines = text.splitlines()
    starts = [(i, m) for i, line in enumerate(lines) if (m := SECTION_RE.match(line))]
    header = "\n".join(lines[:starts[0][0]]) if starts else text

    sections = []
    for idx, (start, match) in enumerate(starts):
        end = starts[idx + 1][0] if idx + 1 < len(starts) else len(lines)
        sections.append((match.group(1), match.group(2), lines[start:end]))
    return header, sections


def main():
    parser = argparse.ArgumentParser(description="Импорт таблицы настроек виджетов в справочник.")
    parser.add_argument("source", help="Путь к WIDGET-SETTINGS-TABLE.md")
    args = parser.parse_args()

    with open(args.source, encoding="utf-8") as f:
        text = f.read()

    header, sections = split_sections(text)
    if not sections:
        print("Не нашёл разделов вида '## Имя (`type`)' — файл другого формата.", file=sys.stderr)
        return 1

    os.makedirs(REFERENCE_DIR, exist_ok=True)
    for name in os.listdir(REFERENCE_DIR):
        if name.startswith("widget-settings-"):
            os.remove(os.path.join(REFERENCE_DIR, name))

    total = 0
    for human_name, wtype, lines in sections:
        path = os.path.join(REFERENCE_DIR, f"widget-settings-{wtype}.md")
        body = "\n".join(lines)
        with open(path, "w", encoding="utf-8") as f:
            f.write(
                f"# Настройки виджета «{human_name}» (`{wtype}`) — справочник свойств\n\n"
                f"Source: Справочник настроек виджетов Fastboard — выгрузка по реальным проектам\n\n"
                f"Ниже — все свойства виджета «{human_name}»: раздел и подраздел настроек, "
                f"название свойства, тип и допустимые значения, а также путь и формат в JSON.\n\n"
                f"{body}\n"
            )
        rows = sum(1 for line in lines if line.startswith("| "))
        total += rows
        print(f"  {human_name} ({wtype}): {rows} строк → {os.path.relpath(path, BASE_DIR)}")

    with open(os.path.join(REFERENCE_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(
            "# Справочник настроек виджетов\n\n"
            "Свойства виджетов Fastboard, собранные по реальным проектам: раздел настроек, "
            "название свойства, тип, допустимые значения и путь в JSON. Того, что здесь есть, "
            "в публичной справке нет — поэтому файлы индексируются в отдельную коллекцию "
            "`widget_settings` и подмешиваются к ответам консультанта.\n\n"
            "Обновление:\n\n"
            "```bash\n"
            "python scripts/import_widget_settings.py путь/к/WIDGET-SETTINGS-TABLE.md\n"
            "python scripts/scrape_and_index.py            # переиндексация\n"
            "```\n\n"
            f"Сводка последней выгрузки:\n\n{header.strip()}\n"
        )

    print(f"\nГотово: {len(sections)} типов виджетов, {total} строк свойств.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
