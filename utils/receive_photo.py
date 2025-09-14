from states import CAPTION, PHOTO
from telegram.ext import ContextTypes
from telegram import Update
from telegram.error import NetworkError, TelegramError
import uuid
import io

async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message.photo:
            await update.message.reply_text("❌ That doesn't seem to be a photo.")
            return PHOTO
        photo_file = await update.message.photo[-1].get_file()
        
        # ✅ Download directly into memory
        bio = io.BytesIO()
        await photo_file.download_to_memory(out=bio)
        bio.seek(0)
        
        # ✅ Store raw data + metadata in context (not Supabase yet)
        context.user_data["photo_bytes"] = bio.getvalue()
        context.user_data["photo_filename"] = f"user_uploads/{uuid.uuid4()}.jpg"
        context.user_data["photo_mime"] = "image/jpeg"
        
        await update.message.reply_text("📝 Got the photo! Now send me the caption.")
        return CAPTION
    except NetworkError:
        await update.message.reply_text("⚠️ Sorry, something went wrong. Please try again shortly.")
    except TelegramError:
        await update.message.reply_text("⚠️ Telegram is currently experiencing issues. Please try again later.")
    except Exception:
        await update.message.reply_text("⚠️ An unexpected error occurred.")