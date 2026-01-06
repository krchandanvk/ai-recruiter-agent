# apps/api/main.py

import os
import sys
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List

# ---- Fix imports path ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from packages.utils.supabase_client import get_supabase_client
from packages.utils.auth import get_jwt

app = FastAPI(title="AI Recruiter Agent")


# -------------------------
# Health Check
# -------------------------
@app.get("/")
def health():
    return {"status": "running"}


# -------------------------
# Request Models
# -------------------------
class JobCreate(BaseModel):
    title: str
    skills: List[str]


# -------------------------
# Create Job (FIXED)
# -------------------------
@app.post("/jobs")
def create_job(
    payload: JobCreate,
    jwt: str = Depends(get_jwt)
):
    """
    Creates a job and auto-attaches recruiter_id
    from authenticated Supabase user (auth.uid)
    """

    supabase = get_supabase_client(jwt)

    # 🔑 Get current user id from JWT
    user_res = supabase.auth.get_user(jwt)

    if not user_res or not user_res.user:
        raise HTTPException(status_code=401, detail="Invalid user")

    recruiter_id = user_res.user.id

    # ✅ Insert job WITH recruiter_id
    data = {
        "title": payload.title,
        "skills": payload.skills,
        "recruiter_id": recruiter_id
    }

    res = supabase.table("jobs").insert(data).execute()

    if res.error:
        raise HTTPException(status_code=400, detail=res.error.message)

    return {
        "message": "Job created successfully",
        "job": res.data[0]
    }
