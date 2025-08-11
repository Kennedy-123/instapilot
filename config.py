from dotenv import load_dotenv
import os
from typing import Final

# Load the .env file
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME: Final = os.getenv("BOT_USERNAME")