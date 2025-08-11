from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError, NetworkError
import logging

logger = logging.getLogger(__name__)


async def start_command(update: Update,  context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        await update.message.reply_text(f"👋 Hey {user.first_name}! I'm instaPilot — your Instagram scheduling assistant. "
                                        "I can help you plan and publish posts effortlessly. 🚀\n\n"
                                        "Type /help to see what I can do!")
    except NetworkError as e:
        logger.error(f"Network error: {e}")
        await update.message.reply_text("⚠️ Sorry, something went wrong. Please try again shortly.")
    except TelegramError as e:
        logger.error(f"Telegram error: {e}")
        await update.message.reply_text("⚠️ Telegram is currently experiencing issues. Please try again later.")
    except Exception as e:
        logger.exception(f"Unexpected error in help_command: {e}")
        await update.message.reply_text("⚠️ An unexpected error occurred.")