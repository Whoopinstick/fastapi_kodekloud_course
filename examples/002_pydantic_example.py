from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn
from typing import Optional

sample = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True # default value so the field is optional
    rating: Optional[int] = None


my_first_post = Post(title="My First Post", content="This is my first post")

print(my_first_post)


# a model in a post request
# fastAPI will validate the data posted matches the schema.
# It will return a response if a field is missing or the wrong data type was sent

# can also convert the pydantic model properties into a dict with model_dump()
# dict() is pydantic1, model_dump is pydantic2

@sample.post("/post")
def post_post(new_post: Post):
    print(new_post.title)
    print(new_post.content)
    print(new_post.published)
    print(new_post.rating)
    print(new_post.model_dump())

"""
Example of a post request sent with title equal to an integer
{
    "detail": [
        {
            "type": "string_type",
            "loc": [
                "body",
                "title"
            ],
            "msg": "Input should be a valid string",
            "input": 1
        }
    ]
}
"""


# create other models based on Posts  for different use cases
# CreatePost and UpdatePost, maybe define different fields that the user should be providing

class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True # default value so the field is optional
    rating: Optional[int] = None

class UpdatePost(BaseModel):
    title: str
    content: str
    published: bool
    rating: Optional[int] = None



# or use inheritance
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass
    # add more fields if needed

class PostUpdate(PostBase):
    pass



if __name__ == "__main__":
    uvicorn.run(sample, host="0.0.0.0", port=8001, reload=True)
