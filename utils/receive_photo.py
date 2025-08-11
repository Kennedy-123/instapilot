from states import CAPTION, PHOTO
from telegram.ext import ContextTypes
from telegram import Update
from telegram.error import NetworkError, TelegramError
import logging

logger = logging.getLogger(__name__)


async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message.photo:
            await update.message.reply_text("❌ That doesn't seem to be a photo.")
            return PHOTO
        photo = update.message.photo[-1].file_id
        context.user_data["photo"] = photo
        await update.message.reply_text("📝 Got the photo! Now send me the caption.")
        return CAPTION
    except NetworkError as e:
        logger.error(f"Network error: {e}")
        await update.message.reply_text("⚠️ Sorry, something went wrong. Please try again shortly.")
    except TelegramError as e:
        logger.error(f"Telegram error: {e}")
        await update.message.reply_text("⚠️ Telegram is currently experiencing issues. Please try again later.")
    except Exception as e:
        logger.exception(f"Unexpected error in help_command: {e}")
        await update.message.reply_text("⚠️ An unexpected error occurred.")