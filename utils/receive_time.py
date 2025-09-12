from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.error import NetworkError, TelegramError
import logging
from datetime import datetime, timezone
from config import supabase
from db.connect_db import SessionLocal
from models.post import Post
from scheduler import scheduler
from apscheduler.triggers.date import DateTrigger
from utils.publish_post import publish_post
import re
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)

async def receive_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_input = update.message.text.strip().replace("：", ":")
        print(f"Received time input: {user_input}")
        
        # ✅ Validate format with regex (HH:MM, 24h)
        if not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", user_input):
            await update.message.reply_text(
                "⚠️ Please send a valid time in HH:MM format (e.g., 14:30)."
            )
            return ConversationHandler.END  # or return TIME to re-ask

        # Validate only time (HH:MM, 24-hour format)
        time_obj = datetime.strptime(user_input, "%H:%M").time()
        context.user_data["time"] = time_obj

        # Upload image to Supabase
        photo = context.user_data.get("photo_bytes")
        if not photo:
            await update.message.reply_text("⚠️ No photo found in session. Please restart.")
            return ConversationHandler.END

        supabase.storage.from_("instapilot-image-bucket").upload(
            path=context.user_data.get("photo_filename"),
            file=photo,
            file_options={"content-type": context.user_data.get("photo_mime")}
        )
        public_url = supabase.storage.from_("instapilot-image-bucket").get_public_url(
            context.user_data["photo_filename"]
        )

        # Save post to database
        scheduled_date = context.user_data.get("date")
        scheduled_datetime = None
        if scheduled_date:
            scheduled_datetime = datetime.combine(
                datetime.strptime(scheduled_date, "%Y-%m-%d").date(),
                time_obj,
                tzinfo=ZoneInfo("Africa/Lagos")
            )

        new_post = Post(
            content=context.user_data.get("caption", ""),
            media_url=public_url,
            scheduled_time=scheduled_datetime,
            published=False,
            author_id=update.effective_user.id,
            created_at=datetime.now(timezone.utc)
        )

        with SessionLocal() as session:
            session.add(new_post)
            session.commit()
            session.refresh(new_post)
            
        # Schedule job
        if scheduled_datetime:
            scheduler.add_job(
                func=publish_post,
                trigger=DateTrigger(run_date=scheduled_datetime),
                args=[new_post.id],
                id=f"post_{new_post.id}",
                replace_existing=True
            )

        await update.message.reply_text(
            f"✅ Scheduled!\n\n"
            f"Photo: saved\n"
            f"Caption: {context.user_data.get('caption', 'N/A')}\n"
            f"Date: {context.user_data.get('date', 'N/A')}\n"
            f"Time: {context.user_data['time']}"
        )
        return ConversationHandler.END
    except NetworkError as e:
        logger.error(f"Network error: {e}")
        await update.message.reply_text("⚠️ Sorry, something went wrong. Please try again shortly.")
    except TelegramError as e:
        logger.error(f"Telegram error: {e}")
        await update.message.reply_text("⚠️ Telegram is currently experiencing issues. Please try again later.")
    except Exception as e:
        logger.exception(f"Unexpected error in receive_time: {e}")
        await update.message.reply_text("⚠️ An unexpected error occurred.")
