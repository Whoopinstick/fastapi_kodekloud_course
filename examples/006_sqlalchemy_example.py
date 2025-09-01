from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import datetime
import uvicorn
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


DB_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/kodekloud_fastapi"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Post(Base):
    __tablename__ = "post"
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


# pydantic models for request/response serialization
# got some error when I tried to use the SQLAlchemy Post() as a parameter in
# async def create_post(post: CreatePost, xxxx
#
class CreatePost(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


# class PostResponse(BaseModel):
#     id: int
#     title: str
#     content: str
#     published: bool
#     created_at: datetime.datetime
#
#     class Config:
#         from_attributes = True
#         # arbitrary_types_allowed = True



# this will create a table in the database if it doesn't exist
# won't update the table definition if the class changes
# Alembic is a library that can run db migrations
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

@app.get("/")
@app.get("/ping")
async def root():
    return {"message": "Hello, World!"}


@app.get("/posts")
async def get_all_posts(db: Session = Depends(get_db)):
    all_posts = db.query(Post).all()
    return {"data": all_posts}



# note, if you want to return the SQL alchemy instance directly ...
# need to uncomment PostResponse class
# change method signature to include response_model -
# @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
# then, change return to just -
# return new_post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: CreatePost, db: Session = Depends(get_db)):
    # annoying if the model has a bunch of fields
    # new_post = Post(title=post.title, content=post.content, published=post.published)

    # unpack the fields
    new_post = Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{post_id}")
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")
    return {"data": post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")
    else:
        db.delete(post)
        db.commit()
        # don't send any data back or any message when something was deleted
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(post_id: int,updated_post: CreatePost, db: Session = Depends(get_db)):
    post_query = db.query(Post).filter(Post.id == post_id)
    post = post_query.first()
    if not post:
        print('no post found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")
    else:
        print('hi')
        post_query.update(updated_post.model_dump())
        db.commit()
        return {"data": post_query.first()}

if __name__ == "__main__":
    print("it's 006")
    uvicorn.run("006_sqlalchemy_example:app", host="0.0.0.0", port=8000, reload=True)

