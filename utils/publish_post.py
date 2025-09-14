from db.connect_db import SessionLocal
from models import *
import requests

GRAPH_API_BASE = "https://graph.facebook.com/v19.0"

def publish_post(post_id: int):
    with SessionLocal() as session:
        post = session.get(Post, post_id)

        if not post or post.published:
            return
        
        # 🔹 Get the author to retrieve access token + IG account ID
        user = session.query(User).filter_by(telegram_id=post.author_id).first()
        if not user or not user.facebook_access_token:
            return
        
        access_token = user.facebook_access_token
        ig_account_id = user.instagram_id
        
        # Step 1: Create a media container
        create_url = f"{GRAPH_API_BASE}/{ig_account_id}/media"
        payload = {
            "image_url": post.media_url,
            "caption": post.content or "",
            "access_token": access_token
        }
        create_res = requests.post(create_url, data=payload).json()
        
        if "id" not in create_res:
            return
        
        creation_id = create_res["id"]
        
        # Step 2: Publish the media container
        publish_url = f"{GRAPH_API_BASE}/{ig_account_id}/media_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": access_token
        }
        publish_res = requests.post(publish_url, data=publish_payload).json()
        
        if "id" not in publish_res:
            return

        post.published = True
        session.commit()
