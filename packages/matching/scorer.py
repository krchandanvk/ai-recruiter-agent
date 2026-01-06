def weighted_score(match: dict) -> float:
    base = match["score"]
    bonus = 0.05 * len(match["extra_skills"])
    penalty = 0.1 * len(match["missing_skills"])

    final = base + bonus - penalty
    return round(max(final, 0.0), 2)
