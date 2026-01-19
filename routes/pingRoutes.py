from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ping3 import ping

ping_router = APIRouter()

@ping_router.get("")

async def ping_host():
    try:
        latency = ping("8.8.8.8", timeout=1)
        return {"latency": latency}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

