"""Общий ответ по документации для Telegram и веб-виджета Фиби.

Промпт, поиск и стриминг — в одном месте. Каналы отличаются только доставкой.
Логика ответа совпадает с scripts/telegram_bot.Rag.answer (актуальный master).
"""

from __future__ import annotations

import logging
import os
import threading
from typing import Callable, Optional

from handoff import HANDOFF_MARK, gate_delta, is_handoff, is_specialist_request
from vision import ollama_chat, ollama_chat_stream

log = logging.getLogger("fb-rag")

WEB_HISTORY_TURNS = int(os.environ.get("WEB_HISTORY_TURNS", os.environ.get("HISTORY_TURNS", "6")))

_rag = None
_rag_lock = threading.Lock()


def get_rag():
    """Один экземпляр Chroma/эмбеддингов на процесс (тот же, что у Telegram)."""
    global _rag
    if _rag is not None:
        return _rag
    with _rag_lock:
        if _rag is not None:
            return _rag
        from telegram_bot import _ensure_rag
        _rag = _ensure_rag()
        return _rag


def truncate_history(history, limit=None):
    """Оставляет последние N сообщений user/assistant."""
    n = WEB_HISTORY_TURNS if limit is None else limit
    if not history or n <= 0:
        return []
    out = []
    for item in history:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = (item.get("content") or "").strip()
        if role not in ("user", "assistant") or not content:
            continue
        out.append({"role": role, "content": content})
    return out[-n:]


def run_answer(rag, question, history=(), extra_context="", search_query=None, on_delta=None):
    """Ядро ответа: поиск → модель → пост-обработка. Telegram и web."""
    from consultant import SYSTEM_PROMPT, build_context
    from telegram_bot import (
        OFFTOPIC_REPLY,
        looks_offtopic,
        doubled_quotes,
        unknown_paths,
        JSON_PATH,
        clean_service_phrases,
    )

    chunks = rag.search_all(search_query or question)

    # Вопрос вне темы: в начатом разговоре отсечка не действует.
    if not extra_context and not history and looks_offtopic(question, chunks):
        log.info("вопрос вне темы — отвечаю без модели")
        if on_delta:
            on_delta(OFFTOPIC_REPLY)
        return OFFTOPIC_REPLY

    context, _sources = build_context(chunks) if chunks else ("", [])
    parts = []
    if extra_context:
        parts.append(
            "Я прислал вложение (изображение или файл). Вот что в нём "
            "(пересказывать содержимое мне не нужно — я его видел, "
            "используй как условие задачи):\n" + extra_context)
    parts.append(f"Вопрос пользователя (отвечай именно на него): {question}")

    system = SYSTEM_PROMPT
    index = rag.article_index()
    if index:
        system += ("\n\nОглавление документации (названия статей и точные ссылки). "
                   "Ссылку для рекомендации бери отсюда, но содержимое статьи, "
                   "которой нет в контексте вопроса, не пересказывай:\n" + index)
    system += ("\n\nКонтекст из документации. Это выдержки, подобранные поиском по "
               "справке под текущий вопрос: пользователь их не присылал и не видит. "
               "Никогда не пиши, что клиент прислал документацию или её фрагменты, и "
               "не путай их с его вложением.\n\n"
               + (context or "(подходящих материалов не нашлось)"))
    messages = [{"role": "system", "content": system}]
    messages += list(history)
    messages.append({"role": "user", "content": "\n\n".join(parts)})

    def publish(full):
        shown = gate_delta(full)
        if shown is False or shown is None:
            return shown is None
        if on_delta:
            on_delta(shown)
        return True

    reply = (ollama_chat_stream(messages, on_delta=publish) if on_delta
             else ollama_chat(messages))
    if is_handoff(reply):
        return HANDOFF_MARK

    if doubled_quotes(reply):
        log.info("кавычки удвоены в правиле — переспрашиваю")
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content":
                         "В ответе кавычки стоят и вокруг подстановки в условии, и "
                         "внутри значения переменной — при подстановке они удвоятся "
                         "и правило упадёт. Выбери ОДИН вариант и выдержи его во всём "
                         "ответе: либо условие `WHERE region = '{{region}}'` со значением "
                         "`Москва` без кавычек, либо условие "
                         "`WHERE region in ( {{regions}} )` со значением `'Москва'` в "
                         "кавычках. Заголовок и примеры не должны противоречить друг "
                         "другу. Покажи, во что превращается условие после подстановки."})
        reply = ollama_chat(messages)

    bad = unknown_paths(reply, context) if context else []
    if bad:
        allowed = sorted(set(JSON_PATH.findall(context)))
        if allowed:
            log.info("выдуманные пути в ответе: %s — переспрашиваю", bad[:3])
            messages.append({"role": "assistant", "content": reply})
            messages.append({"role": "user", "content":
                             "В ответе есть пути, которых нет в таблице свойств: "
                             + ", ".join(bad[:5])
                             + ". Перепиши ответ, используя только эти пути:\n"
                             + "\n".join(allowed[:120])
                             + "\n\nЭто выдержка из таблицы, а не весь список: "
                             + "не утверждай, что других путей не существует."})
            reply = ollama_chat(messages)

        still_bad = unknown_paths(reply, context)
        if still_bad:
            kept = [line for line in reply.splitlines()
                    if not any(bad in line for bad in still_bad)]
            cleaned = "\n".join(kept).strip()
            log.info("убраны строки с выдуманными путями: %s", still_bad[:3])
            if len(cleaned) > 200:
                reply = cleaned
    return clean_service_phrases(reply)


def answer_stream(
    question: str,
    history=(),
    extra_context: str = "",
    search_query: Optional[str] = None,
    on_delta: Optional[Callable[[str], None]] = None,
) -> str:
    """Публичный вход для веб-канала: specialist fast-path + усечённая история."""
    q = (question or "").strip()
    if not q:
        return ""
    if is_specialist_request(q):
        if on_delta:
            on_delta(HANDOFF_MARK)
        return HANDOFF_MARK
    hist = truncate_history(history)
    return run_answer(
        get_rag(),
        q,
        history=hist,
        extra_context=extra_context,
        search_query=search_query,
        on_delta=on_delta,
    )
