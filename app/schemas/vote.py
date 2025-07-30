from pydantic import BaseModel, Field
from typing import Annotated

class Vote(BaseModel):
    post_id: int
    # direction.  1 if they meant to upvote the post.  0 if they want to remove their vote
    dir: Annotated[int, Field(strict=True, ge=0, le=0)]

