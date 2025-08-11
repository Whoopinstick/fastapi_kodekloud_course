from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from alembic import command
from alembic.config import Config

# refactored into app module
# from app.database import Base, engine
from app.routers import posts_router, users_router, auth_router, vote_router

# create database tables if they don't exist
# use Alembic to build database instead
# Base.metadata.create_all(bind=engine)

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    yield

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(posts_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(vote_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}



if __name__ == "__main__":
    # for local development
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
