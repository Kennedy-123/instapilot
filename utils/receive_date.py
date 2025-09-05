from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.error import NetworkError, TelegramError
import logging
from datetime import datetime
from states import TIME
logger = logging.getLogger(__name__)


async def receive_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_input = update.message.text.strip()

        # ✅ Validate date format only
        try:
            scheduled_date = datetime.strptime(user_input, "%Y-%m-%d").date()
        except ValueError:
            await update.message.reply_text(
                "⚠️ Invalid format. Please use `YYYY-MM-DD` (e.g., 2025-09-05)."
            )
            return  # stay in the same state until valid input

        await update.message.reply_text(
            "✅ Date saved!\n\n"
            "⏰ Now send me the time (Use format: `HH:MM`, e.g., 14:30)."
        )

        context.user_data["date"] = str(scheduled_date)

        return TIME
    except NetworkError as e:
        logger.error(f"Network error: {e}")
        await update.message.reply_text("⚠️ Sorry, something went wrong. Please try again shortly.")
    except TelegramError as e:
        logger.error(f"Telegram error: {e}")
        await update.message.reply_text("⚠️ Telegram is currently experiencing issues. Please try again later.")
    except Exception as e:
        logger.exception(f"Unexpected error in help_command: {e}")
        await update.message.reply_text("⚠️ An unexpected error occurred.")
