import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List

from packages.utils.auth import get_jwt
from packages.utils.supabase_client import get_supabase_client
from packages.matching import (
    match_candidate_to_job,
    weighted_score,
    explain_match,
)

app = FastAPI(
    title="AI Recruiter Agent API",
    version="0.1.0",
    openapi_tags=[
        {"name": "Health"},
        {"name": "Jobs"},
        {"name": "Candidates"},
        {"name": "Matching"},
    ],
)

# =========================
# HEALTH
# =========================

@app.get("/", tags=["Health"])
def health():
    return {"status": "ok"}

# =========================
# JOBS
# =========================

class JobCreate(BaseModel):
    title: str
    skills: List[str]

@app.post("/jobs", tags=["Jobs"])
def create_job(
    payload: JobCreate,
    jwt: str = Depends(get_jwt),
):
    supabase = get_supabase_client(jwt)

    res = (
        supabase.table("jobs")
        .insert({
            "title": payload.title,
            "skills": payload.skills,
            "recruiter_id": None,  # filled by RLS via auth.uid()
        })
        .execute()
    )

    return res.data

@app.get("/jobs", tags=["Jobs"])
def list_jobs(jwt: str = Depends(get_jwt)):
    supabase = get_supabase_client(jwt)
    return supabase.table("jobs").select("*").execute().data

# =========================
# CANDIDATES
# =========================

class CandidateCreate(BaseModel):
    job_id: str
    name: str
    skills: List[str]

@app.post("/candidates", tags=["Candidates"])
def create_candidate(
    payload: CandidateCreate,
    jwt: str = Depends(get_jwt),
):
    supabase = get_supabase_client(jwt)

    return (
        supabase.table("candidates")
        .insert({
            "job_id": payload.job_id,
            "name": payload.name,
            "skills": payload.skills,
        })
        .execute()
        .data
    )

@app.get("/candidates", tags=["Candidates"])
def list_candidates(jwt: str = Depends(get_jwt)):
    supabase = get_supabase_client(jwt)
    return supabase.table("candidates").select("*").execute().data

# =========================
# MATCHING
# =========================

@app.get("/jobs/{job_id}/match", tags=["Matching"])
def match_candidates(
    job_id: str,
    jwt: str = Depends(get_jwt),
):
    supabase = get_supabase_client(jwt)

    job = (
        supabase.table("jobs")
        .select("id, skills")
        .eq("id", job_id)
        .single()
        .execute()
        .data
    )

    candidates = (
        supabase.table("candidates")
        .select("id, name, skills")
        .eq("job_id", job_id)
        .execute()
        .data
    )

    results = []

    for c in candidates:
        match = match_candidate_to_job(job["skills"], c["skills"])
        results.append({
            "candidate_id": c["id"],
            "name": c["name"],
            "score": weighted_score(match),
            "explanation": explain_match(match),
            "details": match,
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)
