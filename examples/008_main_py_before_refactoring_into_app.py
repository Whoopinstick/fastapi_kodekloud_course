from datetime import datetime
from fastapi import FastAPI, Response, status, HTTPException, Depends
import uvicorn
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from app.utils import *



DB_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/kodekloud_fastapi"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# pydantic models
class PydanticBasePost(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

class PydanticPostResponse(PydanticBasePost):
    id: int

class PydanticBaseUser(BaseModel):
    email: EmailStr # type to ensure valid email
    password: str

class PydanticUserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class PydanticUserLogin(BaseModel):
    email: EmailStr
    password: str

# sqlalchemy schemas
class AlchemyPost(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='true')
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'), nullable=False)


class AlchemyUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

# path operations
@app.get("/")
async def root():
    return {"message": "Hello World"}


# use the response_model to change which fields are returned
@app.get("/posts/{post_id}", response_model=PydanticPostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(AlchemyPost).filter(AlchemyPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")
    return post

# when using response_model to return multiple items
# need List[] from Typing or receive an error like -
# Input should be a valid dictionary or object to extract fields from
@app.get("/posts", response_model=List[PydanticPostResponse])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(AlchemyPost).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PydanticPostResponse)
async def create_post(post: PydanticBasePost, db: Session = Depends(get_db)):
    new_post = AlchemyPost(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(AlchemyPost).filter(AlchemyPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")
    else:
        db.delete(post)
        db.commit()
        # don't send any data back or any message when something was deleted
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}", response_model=PydanticPostResponse)
async def update_post(post_id: int,updated_post: PydanticBasePost, db: Session = Depends(get_db)):
    post_query = db.query(AlchemyPost).filter(AlchemyPost.id == post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")
    else:
        post_query.update(updated_post.model_dump())
        db.commit()
        return post_query.first()


@app.get("/users/{user_id}", response_model=PydanticUserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(AlchemyUser).filter(AlchemyUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
    else:
        return user


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=PydanticUserResponse)
async def create_user(user: PydanticBaseUser, db: Session = Depends(get_db)):

    # hash the password
    hashed_password = hash_password(user.password)
    user.password = hashed_password

    # save to DB
    new_user = AlchemyUser(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login")
async def login_user(user_credentials: PydanticUserLogin, db: Session = Depends(get_db)):
    user = db.query(AlchemyUser).filter(AlchemyUser.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")

    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    else:
        # create a token and return the token
        return {"token": "abc123"}


if __name__ == "__main__":
    uvicorn.run("008_main_py_before_refactoring_into_app:app", host="0.0.0.0", port=8000, reload=True)
