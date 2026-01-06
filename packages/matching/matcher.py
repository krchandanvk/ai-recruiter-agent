from typing import List, Dict
from .skill_normalizer import normalize_skills

def match_candidate_to_job(
    job_skills: List[str],
    candidate_skills: List[str],
) -> Dict:
    job = set(normalize_skills(job_skills))
    candidate = set(normalize_skills(candidate_skills))

    matched = job & candidate
    missing = job - candidate
    extra = candidate - job

    score = round(len(matched) / max(len(job), 1), 2)

    return {
        "score": score,
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "extra_skills": list(extra),
    }
