import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise RuntimeError("SUPABASE_URL or SUPABASE_ANON_KEY missing")

def get_supabase_client(jwt: str | None = None) -> Client:
    headers = {}
    if jwt:
        headers["Authorization"] = f"Bearer {jwt}"

    return create_client(
        SUPABASE_URL,
        SUPABASE_ANON_KEY,
        headers=headers,
    )
