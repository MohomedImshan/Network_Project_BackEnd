from fastapi import Request, HTTPException
from utils.jwt import verify_access_token

def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = auth_header.split(" ")[1]
    playload = verify_access_token(token)

    if playload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return playload