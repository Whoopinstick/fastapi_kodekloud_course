import uvicorn
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# built in documentation
# /docs
# /redoc

# get request example
@app.get("/")
@app.get("/ping")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/hello")
async def say_hello():
    return {"message": "Hello"}

@app.get("/posts")
async def posts():
    return {"message": "Posts",
            "identifier": 123}


# post request example
@app.post("/postsomething")
async def postsomething():
    return {"message": "You posted something"}

# post request using FastAPI's Body params
# converts the response to a dict
@app.post("/createsomething")
async def createsomething(payload: dict = Body(...)):
    print(payload)
    return {"message": "You created something",
            "title": payload["title"],
            "content": payload["content"]}


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.post("/createsomethingwithvalidation")
async def createsomethingwithvalidation(new_post: Post):
    print(new_post)
    print(new_post.model_dump())
    return {"message": "You created something",
            "title": new_post.title,
            "content": new_post.content,
            "published": new_post.published,
            "rating": new_post.rating}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
