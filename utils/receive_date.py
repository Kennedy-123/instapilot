from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import NetworkError, TelegramError
from datetime import datetime, date, timedelta
from states import TIME, DATE

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
            return DATE
        
        # 🚨 Check if date is in the past
        today = date.today()
        if scheduled_date < today:
            await update.message.reply_text(
                "⚠️ The date you entered has already passed. Please enter a future date."
            )
            return DATE
        
        # 🚨 Check if date is within 60 days
        max_date = today + timedelta(days=60)
        if scheduled_date > max_date:
            await update.message.reply_text(
                "⚠️ Please choose a date within the next 60 days."
            )
            return DATE

        await update.message.reply_text(
            "✅ Date saved!\n\n"
            "⏰ Now send me the time (Use format: `HH:MM`, e.g., 14:30)."
        )

        context.user_data["date"] = str(scheduled_date)

        return TIME
    except NetworkError:
        await update.message.reply_text("⚠️ Sorry, something went wrong. Please try again shortly.")
    except TelegramError:
        await update.message.reply_text("⚠️ Telegram is currently experiencing issues. Please try again later.")
    except Exception:
        await update.message.reply_text("⚠️ An unexpected error occurred.")
