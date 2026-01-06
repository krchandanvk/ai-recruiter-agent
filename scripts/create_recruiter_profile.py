from packages.utils.supabase_client import get_supabase_client

def create_profile(jwt: str, email: str):
    supabase = get_supabase_client(jwt)

    supabase.table("recruiters").insert({
        "email": email
    }).execute()
