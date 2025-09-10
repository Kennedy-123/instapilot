from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from states import PHOTO
from telegram.error import TelegramError, NetworkError
import logging
from utils import check_user_access_token
from dotenv import load_dotenv
import os
from db.connect_db import SessionLocal
from models import User

# Load environment variables from .env
load_dotenv()

LOGIN_URL = os.getenv('LOGIN_URL')
APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')

logger = logging.getLogger(__name__)


def get_user_access_token(telegram_id: int) -> str | None:
    """Fetch the user's access token from db by telegram_id."""
    with SessionLocal() as session:  # create session
        user = session.query(User).filter_by(telegram_id=str(telegram_id)).first()
        if user and user.facebook_access_token:
            return user.facebook_access_token
        return None


async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Notify user we're checking
        await update.message.reply_text("⏳ Checking your Instagram session, please wait...")
        
        telegram_id = update.effective_user.id
        
        # get token from db
        access_token = get_user_access_token(telegram_id)
        

        # check if the token is not valid
        if not access_token:
            login_url = f"{LOGIN_URL}?telegram_id={telegram_id}"
            keyboard = [[InlineKeyboardButton("🔗 Reconnect Facebook", url=login_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                "⚠️ Your Instagram session has expired. Please log in again to continue.",
                reply_markup=reply_markup
            )
            return
        
        # validate token
        is_token_valid = check_user_access_token(access_token=access_token, app_id=APP_ID, app_secret=APP_SECRET)
        
        if not is_token_valid:
            login_url = f"{LOGIN_URL}?telegram_id={telegram_id}"
            keyboard = [[InlineKeyboardButton("🔗 Reconnect Facebook", url=login_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                "⚠️ Your Instagram session has expired. Please log in again to continue.",
                reply_markup=reply_markup,
            )
            return

        await update.message.reply_text("📸 Please send the image you want to schedule.")
        return PHOTO
    except NetworkError as e:
        logger.error(f"Network error: {e}")
        await update.message.reply_text("⚠️ Sorry, something went wrong. Please try again shortly.")
    except TelegramError as e:
        logger.error(f"Telegram error: {e}")
        await update.message.reply_text("⚠️ Telegram is currently experiencing issues. Please try again later.")
    except Exception as e:
        logger.exception(f"Unexpected error in help_command: {e}")
        await update.message.reply_text("⚠️ An unexpected error occurred.")
