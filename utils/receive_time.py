from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.error import NetworkError, TelegramError
from datetime import datetime, timezone
from config import supabase
from db.connect_db import SessionLocal
from models.post import Post
from scheduler import scheduler
from apscheduler.triggers.date import DateTrigger
from utils.publish_post import publish_post
import re
from zoneinfo import ZoneInfo
from states import TIME

async def receive_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_input = update.message.text.strip().replace("：", ":")

        # ✅ Validate format with regex (HH:MM, 24h)
        if not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", user_input):
            await update.message.reply_text(
                "⚠️ Please send a valid time in HH:MM format (e.g., 14:30)."
            )
            return TIME  # stay in TIME state and re-ask

        # Parse time
        time_obj = datetime.strptime(user_input, "%H:%M").time()
        context.user_data["time"] = time_obj

        # Combine with date from context
        scheduled_date = context.user_data.get("date")
        scheduled_datetime = None
        if scheduled_date:
            scheduled_datetime = datetime.combine(
                datetime.strptime(scheduled_date, "%Y-%m-%d").date(),
                time_obj,
                tzinfo=ZoneInfo("Africa/Lagos"),
            )

        # Ensure time is in the future
        if scheduled_datetime <= datetime.now(ZoneInfo("Africa/Lagos")):
            await update.message.reply_text(
                "⚠️ The time you entered has already passed. Please enter a future time."
            )
            return TIME

        # Get photo from session
        photo = context.user_data.get("photo_bytes")
        if not photo:
            await update.message.reply_text("⚠️ No photo found in session. Please restart.")
            return ConversationHandler.END

        bucket = supabase.storage.from_("instapilot-image-bucket")
        photo_filename = context.user_data.get("photo_filename")

        # ✅ Check if image exists → update, else upload
        try:
            existing_files = bucket.list(path=photo_filename)
            if existing_files:  
                bucket.update(
                    path=photo_filename,
                    file=photo,
                    file_options={"content-type": context.user_data.get("photo_mime")},
                )
            else:
                bucket.upload(
                    path=photo_filename,
                    file=photo,
                    file_options={"content-type": context.user_data.get("photo_mime")},
                )
        except Exception:
            await update.message.reply_text("⚠️ Failed to upload image. Please try again.")
            return ConversationHandler.END

        # Get public URL
        public_url = bucket.get_public_url(photo_filename)

        # Save post in DB
        new_post = Post(
            content=context.user_data.get("caption", ""),
            media_url=public_url,
            scheduled_time=scheduled_datetime,
            published=False,
            author_id=update.effective_user.id,
            created_at=datetime.now(timezone.utc),
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
                replace_existing=True,
            )

        await update.message.reply_text(
            f"✅ Scheduled!\n\n"
            f"Photo: saved\n"
            f"Caption: {context.user_data.get('caption', 'N/A')}\n"
            f"Date: {context.user_data.get('date', 'N/A')}\n"
            f"Time: {context.user_data['time']}"
        )
        return ConversationHandler.END

    except NetworkError:
        await update.message.reply_text("⚠️ Sorry, something went wrong. Please try again shortly.")
    except TelegramError:
        await update.message.reply_text("⚠️ Telegram is currently experiencing issues. Please try again later.")
    except Exception:
        await update.message.reply_text("⚠️ An unexpected error occurred. Try again later.")
        return ConversationHandler.END