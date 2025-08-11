from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError, NetworkError
import logging

logger = logging.getLogger(__name__)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            "Here’s what I can help you with:\n"
            "/schedule – Schedule a new post 📅\n"
            "/status – Check your scheduled posts 📋\n"
            "/cancel – Cancel a scheduled post ❌\n"
            "/connect - Login via facebook \n"
        )
    except NetworkError as e:
        logger.error(f"Network error: {e}")
        await update.message.reply_text("⚠️ Sorry, something went wrong. Please try again shortly.")
    except TelegramError as e:
        logger.error(f"Telegram error: {e}")
        await update.message.reply_text("⚠️ Telegram is currently experiencing issues. Please try again later.")
    except Exception as e:
        logger.exception(f"Unexpected error in help_command: {e}")
        await update.message.reply_text("⚠️ An unexpected error occurred.")
