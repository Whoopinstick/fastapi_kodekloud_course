import uvicorn
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import random

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    id: Optional[int] = None

all_posts = []

# create new post, response code is 200
@app.post("/posts_one")
async def posts(post: Post):
    post.id = random.randint(1,100_000_000)
    new_post_dict = post.model_dump()
    print(new_post_dict)
    all_posts.append(new_post_dict)
    print(all_posts)
    return {"data": new_post_dict}

# create new post, change default status code to 201
@app.post("/posts_two", status_code=status.HTTP_201_CREATED)
async def posts(post: Post):
    post.id = random.randint(1,100_000_000)
    new_post_dict = post.model_dump()
    print(new_post_dict)
    all_posts.append(new_post_dict)
    print(all_posts)
    return {"data": new_post_dict}



# get request, but a 200 response is still returned even if no matching post is found
@app.get("/posts_example_one/{post_id}")
def post_by_id_one(post_id: int):
    global all_posts
    for post in all_posts:
        if post["id"] == post_id:
            return {"data": post}
        return {"message": f"Post {post_id} not found"}
    return {"message": f"Post {post_id} not found"}



# get request, change response code to 404
@app.get("/posts_example_two/{post_id}")
def post_by_id_two(post_id: int, response: Response):
    global all_posts
    for post in all_posts:
        if post["id"] == post_id:
            return {"data": post}
        # change status code from 200 to 404 if no match found

        # instead of hard coding status, pick from enum
        # response.status_code = 404
        response.status_code = status.HTTP_404_NOT_FOUND

        return {"message": f"Post {post_id} not found"}
    # change status code from 200 to 404 if no match found

    # instead of hard coding status, pick from enum
    # response.status_code = 404
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": f"Post {post_id} not found"}


# get request, change response code to 404 by raising exception
@app.get("/posts_example_two/{post_id}")
def post_by_id_two(post_id: int):
    global all_posts
    for post in all_posts:
        if post["id"] == post_id:
            return {"data": post}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")