import re
from typing import List

COMMON_ALIASES = {
    "fast api": "fastapi",
    "react.js": "react",
    "node js": "nodejs",
    "postgres": "postgresql",
    "postgre sql": "postgresql",
}

def normalize_skill(skill: str) -> str:
    skill = skill.lower().strip()
    skill = re.sub(r"[^a-z0-9+.#]", " ", skill)
    skill = re.sub(r"\s+", " ", skill)
    return COMMON_ALIASES.get(skill, skill)


def normalize_skills(skills: List[str]) -> List[str]:
    return sorted(set(normalize_skill(s) for s in skills))
