# agents/matching_agent/matching_agent.py

def match_candidates(job: dict, candidates: list):
    results = []

    job_skills = set(job.get("skills", []))

    for c in candidates:
        candidate_skills = set(c.get("skills", []))
        matched = job_skills & candidate_skills
        score = len(matched) * 25

        results.append({
            "candidate": c.get("name"),
            "score": score,
            "matched_skills": list(matched),
            "verdict": "STRONG FIT" if score >= 50 else "PARTIAL FIT"
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)
