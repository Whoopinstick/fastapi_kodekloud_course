from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
import app.models as models
from app.schemas import BaseUser, UserResponse
from app.utils import *

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
    else:
        return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: BaseUser, db: Session = Depends(get_db)):

    # hash the password
    hashed_password = hash_password(user.password)
    user.password = hashed_password

    # save to DB
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user