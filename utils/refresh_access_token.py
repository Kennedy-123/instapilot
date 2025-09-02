import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def refresh_access_token(old_token: str) -> tuple[str | None, int | None]:
    """
    Refresh a valid long-lived Instagram user access token.
    Returns a tuple of (new_token, expires_in_seconds) or (None, None) on failure.
    """
    url = "https://graph.instagram.com/refresh_access_token"
    params = {
        "grant_type": "ig_refresh_token",
        "access_token": old_token
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        new_token = data.get("access_token")
        expires_in = data.get("expires_in")
        return new_token, expires_in
    except requests.RequestException as e:
        # Optionally log the error
        print(f"[refresh_long_lived_token] Error refreshing token: {e}")
        return None, None
