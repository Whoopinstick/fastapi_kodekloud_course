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