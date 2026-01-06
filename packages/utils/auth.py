# packages/utils/auth.py

from fastapi import Header, HTTPException

def get_jwt(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")

    return authorization.replace("Bearer ", "")
