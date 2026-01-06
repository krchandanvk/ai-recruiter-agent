def screen_candidate(answers: dict):
    score = sum(answers.values())

    return {
        "score": score,
        "decision": "PASS" if score >= 70 else "HOLD"
    }
