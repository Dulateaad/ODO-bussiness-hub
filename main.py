import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# Настройки
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Токен из переменных окружения
TARGET_URL = "https://studio--studio-122846357-42699.us-central1.hosted.app"
PORT = int(os.getenv("PORT", 8080))
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL")  # Render сам подставит URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Открыть Studio", url=TARGET_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Привет! Нажмите кнопку, чтобы открыть Studio:",
        reply_markup=reply_markup
    )

def main():
    if not TOKEN:
        raise ValueError("❌ BOT_TOKEN не задан!")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Запуск как webhook для Render
    logger.info("🚀 Запуск бота через webhook...")
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{WEBHOOK_URL}/webhook"
    )

if __name__ == "__main__":
    main()
