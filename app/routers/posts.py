from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.database import get_db
import app.models as models
from app.oauth2 import get_current_user
from app.schemas import BasePost, PostResponse, PostVote

router = APIRouter(prefix="/posts", tags=["posts"])


# use the response_model to change which fields are returned
@router.get("/{post_id}", response_model=PostVote)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    # comment out to add voting
    # post = db.query(models.Post).filter(models.Post.id == post_id).first()

    result = ((db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
               .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
               .group_by(models.Post.id))
              .filter(models.Post.id == post_id).first())

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")

    post, vote_count = result

    # Transform the query result to match the schema
    post_data = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "published": post.published,
        "user_id": post.user_id,
        "user": post.user,
        "votes": vote_count or 0
    }

    return post_data

# when using response_model to return multiple items
# need List[] from Typing or receive an error like -
# Input should be a valid dictionary or object to extract fields from
@router.get("/", response_model=List[PostVote])
# original route before updating the response model to join posts to votes
# @router.get("/", response_model=List[PostResponse])
# original method signature before adding query parameters
# async def get_posts(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
async def get_posts(db: Session = Depends(get_db), limit: int = 100, skip: int = 0, search: Optional[str] = ""):

        results = ((db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
                    .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
                    .group_by(models.Post.id))
                   .filter(models.Post.title.contains(search)).limit(limit).offset(skip).all())

        if not results:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")

        # Transform the query results to match the schema
        posts = []
        for post, vote_count in results:
            post_dict = {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "published": post.published,
                "user_id": post.user_id,
                "user": post.user,
                "votes": vote_count
            }
            posts.append(post_dict)

        return posts




    # # testing out query parameters
    # print(limit)
    # print(skip)
    # print(search)
    #
    # # update ORM to limit, skip, and filter/search
    # # original query before joining to Vote
    # # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #
    # # join to votes table, add sqlalchemy function to count by and change the label of the column
    # # group by Post.id
    # #
    # posts = ((db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
    #            .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
    #            .group_by(models.Post.id))
    #            .filter(models.Post.title.contains(search)).limit(limit).offset(skip).all())
    #
    # print(posts)
    #
    # # if you wanted to filter the posts created by that user, change method signature, and add filter()
    # # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id)
    # if not posts:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    # return posts


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
