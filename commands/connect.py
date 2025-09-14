from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

LOGIN_URL = os.getenv('LOGIN_URL')

async def connect_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    login_url = f"{LOGIN_URL}?telegram_id={telegram_id}"

    keyboard = [
        [InlineKeyboardButton("🔗 Login with Facebook", url=login_url)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Please log in with Facebook to connect your Instagram account:",
        reply_markup=reply_markup
    )