# apps/api/main.py

from fastapi import FastAPI, Depends
from packages.utils.supabase_client import get_supabase_client
from packages.utils.auth import get_jwt

app = FastAPI(title="AI Recruiter Agent")

@app.post("/jobs")
def create_job(payload: dict, jwt: str = Depends(get_jwt)):
    """
    Creates a job owned by the authenticated recruiter
    """
    supabase = get_supabase_client(jwt)

    # 1️⃣ Get authenticated user ID
    user = supabase.auth.get_user(jwt)
    recruiter_id = user.user.id

    # 2️⃣ Parse JD → skills (simplified for now)
    title = "Software Engineer"
    skills = ["Python", "FastAPI", "SQL"]

    # 3️⃣ Insert job WITH recruiter_id
    result = supabase.table("jobs").insert({
        "title": title,
        "skills": skills,
        "recruiter_id": recruiter_id
    }).execute()

    return result.data
