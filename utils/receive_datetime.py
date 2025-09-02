from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.error import NetworkError, TelegramError
import logging

logger = logging.getLogger(__name__)

async def receive_datetime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["datetime"] = update.message.text
        await update.message.reply_text(
            f"✅ Scheduled!\n\nPhoto: saved\nCaption: {context.user_data['caption']}\nDatetime: {context.user_data['datetime']}"
        )
        return ConversationHandler.END
    except NetworkError as e:
        logger.error(f"Network error: {e}")
        await update.message.reply_text("⚠️ Sorry, something went wrong. Please try again shortly.")
    except TelegramError as e:
        logger.error(f"Telegram error: {e}")
        await update.message.reply_text("⚠️ Telegram is currently experiencing issues. Please try again later.")
    except Exception as e:
        logger.exception(f"Unexpected error in help_command: {e}")
        await update.message.reply_text("⚠️ An unexpected error occurred.")