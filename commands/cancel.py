from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.error import NetworkError, TelegramError

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("❌ Scheduling cancelled.")
        return ConversationHandler.END
    except NetworkError as e:
        await update.message.reply_text("⚠️ Sorry, something went wrong. Please try again shortly.")
    except TelegramError as e:
        await update.message.reply_text("⚠️ Telegram is currently experiencing issues. Please try again later.")
    except Exception as e:
        await update.message.reply_text("⚠️ An unexpected error occurred.")
