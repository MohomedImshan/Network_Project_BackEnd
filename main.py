from fastapi import FastAPI
from core.database import engine
from models.models import Base
from routes.auth import router as auth_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth")

@app.get("/")
def root():
    return {"status": "Backend running"}
