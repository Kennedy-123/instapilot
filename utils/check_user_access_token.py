import requests

def check_user_access_token(access_token, app_id, app_secret):
    """Check if token is valid using /debug_token"""
    debug_url = "https://graph.facebook.com/debug_token"
    params = {
        "input_token": access_token,
        "access_token": f"{app_id}|{app_secret}"
    }
    
    try:
        res = requests.get(debug_url, params=params, timeout=10)
        data = res.json().get("data", {})
        return data.get("is_valid", False)
    except requests.RequestException as e:
        print(f"⚠️ Token check failed: {e}")
        return False
