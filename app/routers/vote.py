from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
import app.models as models
from app.schemas import Vote
from app.oauth2 import get_current_user


router = APIRouter(prefix="/vote", tags=["vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(user_vote: Vote, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == user_vote.post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f"Post {user_vote.post_id} not found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == user_vote.post_id,
                                              models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()
    if user_vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted")
        else:
            new_vote = models.Vote(post_id=user_vote.post_id,user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            return "Successfully added vote"
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return "Successfully removed vote"
