#!/usr/bin/env python3
"""Telegram-бот: AI-консультант по Fastboard и ClickHouse (OpenRouter + RAG).

Режим polling — публичный URL/вебхук не нужен. Запуск:
    TELEGRAM_BOT_TOKEN=... OPENROUTER_API_KEY=... python scripts/telegram_bot.py
"""

import os
import asyncio
import logging

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from rag_common import CHAT_MODEL, EMBEDDING_MODEL
from consultant import Consultant

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO
)
log = logging.getLogger("fastboard-bot")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TOP_K = int(os.environ.get("BOT_TOP_K", "6"))
DEFAULT_SOURCE = os.environ.get("BOT_SOURCE", "both")  # fastboard | clickhouse | both
TG_LIMIT = 4096

WELCOME = (
    "👋 Я AI-консультант по Fastboard и ClickHouse.\n\n"
    "Просто задайте вопрос обычным текстом, например:\n"
    "• Как создать дашборд в Fastboard?\n"
    "• Что такое движок MergeTree?\n\n"
    "Команды: /help — справка."
)


def _split(text: str, limit: int = TG_LIMIT):
    """Режет длинный ответ на части по лимиту Telegram, по возможности по строкам."""
    parts = []
    while len(text) > limit:
        cut = text.rfind("\n", 0, limit)
        if cut <= 0:
            cut = limit
        parts.append(text[:cut])
        text = text[cut:].lstrip("\n")
    if text:
        parts.append(text)
    return parts


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Задайте вопрос текстом — я найду ответ в документации и приведу источники.\n"
        f"Модель: {CHAT_MODEL}. Источники: Fastboard и ClickHouse."
    )


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = (update.message.text or "").strip()
    if not question:
        return

    consultant: Consultant = context.application.bot_data["consultant"]
    await update.message.chat.send_action(ChatAction.TYPING)

    try:
        # consultant.answer синхронный (сетевые вызовы) — уводим в поток,
        # чтобы не блокировать event loop бота
        reply = await asyncio.to_thread(
            consultant.answer, question, DEFAULT_SOURCE, TOP_K, CHAT_MODEL
        )
    except Exception as e:  # noqa: BLE001
        log.exception("Ошибка при обработке вопроса")
        reply = f"⚠️ Не удалось получить ответ: {e}"

    for chunk in _split(reply):
        await update.message.reply_text(chunk, disable_web_page_preview=True)


def main():
    if not TELEGRAM_BOT_TOKEN:
        raise SystemExit("Не задан TELEGRAM_BOT_TOKEN (в .env или окружении).")

    log.info("Старт бота: чат=%s, эмбеддинги=%s", CHAT_MODEL, EMBEDDING_MODEL)

    # Инициализируем консультанта один раз (проверит ключ и подключение к ChromaDB)
    consultant = Consultant()

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.bot_data["consultant"] = consultant
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))

    log.info("Бот запущен (polling). Ctrl+C для остановки.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
