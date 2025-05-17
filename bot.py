import logging
import os
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Load tokens from environment variables
TELEGRAM_TOKEN = os.getenv("8162609784:AAG3gzfROSiRZevvbh6GNLjuK3xTV2hL3vg")
OPENAI_API_KEY = os.getenv("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")

# Set up OpenAI
openai.api_key = OPENAI_API_KEY

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm ChatGPT bot. Ask me anything.")

# Handle messages
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_msg}],
            max_tokens=1000,
            temperature=0.7,
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI Error: {e}")
        bot_reply = "❌ Sorry, there was a problem with the OpenAI API."

    await update.message.reply_text(bot_reply)

# Main function
async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    logger.info("Bot started...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
