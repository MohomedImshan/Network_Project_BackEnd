from fastapi import FastAPI
from core.database import engine
from models.User import Base
from routes.userRoutes import router as user_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router, prefix="/user")

@app.get("/")
def root():
    return {"status": "Backend running"}
