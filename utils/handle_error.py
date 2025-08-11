import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Global error handler for the bot."""

    # Log full traceback for debugging
    logger.error("⚠️ Exception while handling an update:", exc_info=context.error)

    # Only try to respond if it's a Telegram Update
    if isinstance(update, Update):
        try:
            # If the error happened in a message-based handler
            if update.message:
                await update.message.reply_text(
                    "⚠️ Something went wrong. Please try again in a moment."
                )
            # If the error happened during a button press (callback query)
            elif update.callback_query:
                await update.callback_query.answer(
                    "⚠️ An error occurred. Please try again.", show_alert=True
                )
        except Exception as e:
            logger.warning(f"⚠️ Failed to send error message to user: {e}")
