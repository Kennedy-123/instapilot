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


# def is_token_valid(access_token, app_id, app_secret):
#     """Check if token is valid using /debug_token"""
#     debug_url = "https://graph.facebook.com/debug_token"
#     params = {
#         "input_token": access_token,
#         "access_token": f"{app_id}|{app_secret}"
#     }
#     res = requests.get(debug_url, params=params)
#     if res.status_code != 200:
#         print("⚠️ Token check failed:", res.json())
#         return False
#
#     data = res.json().get("data", {})
#     return data.get("is_valid", False)


def exchange_for_long_lived_token(short_token, app_id, app_secret):
    """Exchange short-lived token for long-lived"""
    exchange_url = "https://graph.facebook.com/v19.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_token
    }
    res = requests.get(exchange_url, params=params)
    if res.status_code == 200:
        new_token = res.json().get("access_token")
        print("🔁 Exchanged for long-lived token.")
        return new_token
    else:
        print("❌ Failed to exchange token:", res.json())
        return None


# Step 0: Validate or exchange access token
if not is_token_valid(ACCESS_TOKEN, APP_ID, APP_SECRET):
    print("⚠️ Access token may be expired or short-lived. Attempting to exchange...")
    new_token = exchange_for_long_lived_token(ACCESS_TOKEN, APP_ID, APP_SECRET)
    if new_token and is_token_valid(new_token, APP_ID, APP_SECRET):
        ACCESS_TOKEN = new_token
        print("✅ Using new long-lived token.")
    else:
        print("❌ Could not recover from token failure.")
        exit()

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
