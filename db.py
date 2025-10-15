import os
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

def is_verified(user_id):
    res = requests.get(f"{SUPABASE_URL}/rest/v1/users?user_id=eq.{user_id}", headers=HEADERS)
    return len(res.json()) > 0

def save_user(user_id):
    data = {"user_id": user_id}
    requests.post(f"{SUPABASE_URL}/rest/v1/users", json=data, headers=HEADERS)

def get_verified_users():
    res = requests.get(f"{SUPABASE_URL}/rest/v1/users", headers=HEADERS)
    return [u["user_id"] for u in res.json()]
