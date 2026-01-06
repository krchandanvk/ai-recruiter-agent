# apps/api/main.py

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fastapi import FastAPI, Depends
from packages.utils.supabase_client import get_supabase_client
from packages.utils.auth import get_jwt
from agents.jd_agent.jd_agent import parse_jd
from agents.matching_agent.matching_agent import match_candidates

app = FastAPI(title="AI Recruiter Agent")

@app.get("/")
def health():
    return {"status": "running"}

# 🔐 Create Job (AUTH REQUIRED)
@app.post("/jobs")
def create_job(payload: dict, jwt: str = Depends(get_jwt)):
    supabase = get_supabase_client(jwt)

    parsed = parse_jd(payload["jd"])

    res = supabase.table("jobs").insert({
        "title": parsed["title"],
        "skills": parsed["skills"],
        "recruiter_id": "auth.uid()"
    }).execute()

    return res.data

# 🧠 Match logic (no auth required yet)
@app.post("/match")
def match(payload: dict):
    return match_candidates(
        payload["job"],
        payload["candidates"]
    )
