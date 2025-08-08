from pydantic import BaseModel
from typing import Optional
from .user import UserResponse

class BasePost(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

class PostResponse(BasePost):
    id: int
    user_id: int
    user: UserResponse



# response model for joining posts to votes
# class PostVote(BasePost):
#     Post: PostResponse
#     votes: int

# remove subclassing for debugging
class PostVote(BaseModel):
    id: int
    title: str
    content: str
    published: Optional[bool] = True
    user_id: int
    user: UserResponse
    votes: int
