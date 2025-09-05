import requests
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
IG_USER_ID = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')

IMAGE_URL = "https://www.patterns.dev/img/reactjs/react-logo@3x.svg"
CAPTION = "🚀 Hello from the Instagram Graph API!"

# Step 1: Create media container
create_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
create_params = {
    "image_url": IMAGE_URL,
    "caption": CAPTION,
    "access_token": ACCESS_TOKEN
}

create_res = requests.post(create_url, data=create_params)

if create_res.status_code != 200:
    print("❌ Failed to create media container")
    print(create_res.json())
    exit()

creation_id = create_res.json().get("id")
print("✅ Media container created with ID:", creation_id)

# Step 2: Wait for container to be ready
time.sleep(2)

# Step 3: Publish the post
publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
publish_params = {
    "creation_id": creation_id,
    "access_token": ACCESS_TOKEN
}

publish_res = requests.post(publish_url, data=publish_params)

if publish_res.status_code == 200:
    print("✅ Post published successfully!")
    print("Instagram Post ID:", publish_res.json().get("id"))
else:
    print("❌ Failed to publish post")
    print(publish_res.json())
