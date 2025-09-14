from telegram import Update
from telegram.ext import ContextTypes
from .handle_response import handle_response
from config import BOT_USERNAME
from telegram.error import TelegramError, NetworkError


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message_type: str = update.message.chat.type
        text: str = update.message.text

        if message_type == 'group':
            if BOT_USERNAME in text:
                new_text: str = text.replace(BOT_USERNAME, '').strip()
                response: str = handle_response(new_text)
            else:
                return
        else:
            response: str = handle_response(text)

        if response:
            await update.message.reply_text(response)
    except NetworkError:
        await update.message.reply_text("⚠️ Sorry, something went wrong. Please try again shortly.")
    except TelegramError:
        await update.message.reply_text("⚠️ Telegram is currently experiencing issues. Please try again later.")
    except Exception:
        await update.message.reply_text("⚠️ An unexpected error occurred.")
