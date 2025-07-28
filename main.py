from fastapi import FastAPI
import uvicorn

# refactor into app module
from app.database import Base, engine
from app.routers import posts_router, users_router, auth_router

# create database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts_router)
app.include_router(users_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
