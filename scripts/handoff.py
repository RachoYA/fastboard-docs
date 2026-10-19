"""Просьба о живом специалисте: локальный скор и маркер для потока.

Очевидные фразы решаются здесь, без модели. Перефраз ловит сам ответ:
модель пишет ровно [[HANDOFF]] и останавливается. Второй вызов классификации нет.
"""

import re

HANDOFF_MARK = "[[HANDOFF]]"
THRESHOLD = 0.8

# Канал без формы (CLI) не показывает маркер пользователю.
CLI_HANDOFF = (
    "Чтобы связаться со специалистом, в Telegram-боте отправьте команду /human."
)

_INTENTS = (
    ("strong", re.compile(r"позвать|позови(?:те)?", re.I)),
    ("strong", re.compile(r"позов\w*.{0,40}специалист", re.I)),
    ("strong", re.compile(r"с кем связат|как связаться|свяжите|соедините|переключите|переведите", re.I)),
    ("strong", re.compile(r"дайте контакт", re.I)),
    ("strong", re.compile(r"нуж(?:ен|на|ны|но).{0,24}(специалист|человек|оператор|сотрудник|поддерж)", re.I)),
    ("strong", re.compile(r"хочу (поговорить|пообщаться).{0,40}(человек|оператор|специалист|сотрудник)", re.I)),
    ("strong", re.compile(r"жив(?:ой|ого) человек", re.I)),
    ("strong", re.compile(r"тех\.?\s?поддерж|служб\w*.{0,12}поддерж|служб\w* забот", re.I)),
    ("strong", re.compile(
        r"(свяж|соедин|переключ|позов|пообща|поговори).{0,40}(поддерж|специалист|оператор|сотрудник)", re.I)),
    ("strong", re.compile(r"верните меня к человеку|ты не помог|бот не помог|мне нужен оператор", re.I)),
    ("strong", re.compile(
        r"\b(call|talk to|connect me|transfer me|live)\b.{0,24}\b(human|person|agent|operator|specialist|support)\b",
        re.I)),
    ("strong", re.compile(r"\b(need|want)\b.{0,16}\b(a )?(human|operator|agent|specialist)\b", re.I)),
    ("weak", re.compile(r"\b(operator|support|agent|specialist)\b", re.I)),
    ("weak", re.compile(r"(?:^|\W)(оператор\w*|поддержк\w*|специалист\w*)(?:\W|$)", re.I)),
    ("weak", re.compile(r"^(help|помощь)[.!?]?$", re.I)),
)


def is_specialist_request(text):
    t = (text or "").strip()
    if not t:
        return False
    n = len(t.split())
    score = 0.0
    for tier, pat in _INTENTS:
        if not pat.search(t):
            continue
        score += 1.0 if tier == "strong" else (0.85 if n <= 2 else 0.35)
    return score >= THRESHOLD


def is_handoff(text):
    return (text or "").lstrip().startswith(HANDOFF_MARK)


def gate_delta(full):
    """None — префикс маркера, ещё не показывать. False — это handoff, стоп. Иначе текст."""
    t = (full or "").lstrip()
    if not t or (HANDOFF_MARK.startswith(t) and not t.startswith(HANDOFF_MARK)):
        return None
    if t.startswith(HANDOFF_MARK):
        return False
    return full
