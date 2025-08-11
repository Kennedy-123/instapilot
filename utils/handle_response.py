def handle_response(text: str) -> str:
    text = text.lower().strip()

    if "hello" in text or "hi" in text or 'hey' in text:
        return "Hey there! 👋 I'm instaPilot. Ready to help you schedule your next Instagram post. 📸"
    elif "how are you" in text:
        return "I'm doing great, thanks for asking! 🤖 How can I help you today?"
    elif "schedule" in text:
        return "Awesome! 🗓️ Send me the image, caption, and the time you'd like me to post."
    elif "help" in text:
        return "Here's what I can do:\n/schedule – Schedule a post\n/status – View scheduled posts\n/cancel – Cancel a post"
    else:
        return "Hmm, I didn't quite get that 🤔. Try typing /help to see what I can do."
