from telegram import Update
from telegram.ext import ContextTypes
from states import DATE, CAPTION
from telegram.error import TelegramError, NetworkError

async def receive_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        caption = update.message.text
        if not caption:
            await update.message.reply_text("⚠️ Please send a text caption.")
            return CAPTION
        
        context.user_data["caption"] = caption
        await update.message.reply_text("⏰ When should I post it? (Use format: `YYYY-MM-DD`)")
        return DATE
    except NetworkError:
        await update.message.reply_text("⚠️ Sorry, something went wrong. Please try again shortly.")
    except TelegramError:
        await update.message.reply_text("⚠️ Telegram is currently experiencing issues. Please try again later.")
    except Exception:
        await update.message.reply_text("⚠️ An unexpected error occurred.")
