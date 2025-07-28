from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
import app.models as models
from app.oauth2 import get_current_user
from app.schemas import BasePost, PostResponse


router = APIRouter(prefix="/posts", tags=["posts"])


# use the response_model to change which fields are returned
@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")
    return post

# when using response_model to return multiple items
# need List[] from Typing or receive an error like -
# Input should be a valid dictionary or object to extract fields from
@router.get("/", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db), limit: int = 100, skip: int = 0, search: Optional[str] = ""):
# async def get_posts(db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    # testing out query parameters
    print(limit)
    print(skip)
    print(search)

    # update ORM to limit, skip, and filter/search
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # if you wanted to filter the posts created by that user, change method signature, and add filter()
    # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id)
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    return posts

# protected route, since it depends on the get_current_user function
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(post: BasePost, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    print(current_user.email)
    new_post = models.Post(**post.model_dump())
    # add the current logged-in user's id as the posts.user_id after adding FK
    new_post.user_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")
    else:
        if current_user.id == post.user_id:
            # allow the user to delete the post if it's theirs
            db.delete(post)
            db.commit()
            # don't send any data back or any message when something was deleted
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            # raise an exception if a user tries to delete someone else's post
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You are not authorized to perform this action")


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(post_id: int,updated_post: BasePost, db: Session = Depends(get_db),
                      current_user = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")
    else:
        if post.user_id == current_user.id:
            post_query.update(updated_post.model_dump())
            db.commit()
            return post_query.first()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to perform this action")
