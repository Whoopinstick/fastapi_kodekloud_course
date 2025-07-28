from datetime import datetime
from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    email: EmailStr # type to ensure valid email
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime