def explain_match(match: dict) -> str:
    return (
        f"Matched {len(match['matched_skills'])} skills. "
        f"Missing {len(match['missing_skills'])}. "
        f"Extra {len(match['extra_skills'])}."
    )
