from telegram.ext import Application, CommandHandler, filters, MessageHandler, ConversationHandler
from commands import *
from states import PHOTO, DATE, CAPTION, TIME
from utils import *
from config import TOKEN


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("schedule", schedule_command)],
    states={
        PHOTO: [MessageHandler(filters.PHOTO, receive_photo)],
        CAPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_caption)],
        DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_date)],
        TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_time)]
    },
    fallbacks=[CommandHandler("cancel", cancel_command)],
    allow_reentry=True
)


if __name__ == '__main__':
    print("Staring bot...")
    app = Application.builder().token(TOKEN).build()

    # 🔹 1. Conversation Handler — should be first to catch multi-step commands early
    app.add_handler(conv_handler)

    # commands handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('connect', connect_command))

    # Messages Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors Handler
    app.add_error_handler(error_handler)

    print('polling...')
    app.run_polling(poll_interval=3)