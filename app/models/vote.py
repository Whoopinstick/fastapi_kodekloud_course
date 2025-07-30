from app.database import Base
from sqlalchemy import Column, Integer, ForeignKey


class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"),  primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),  primary_key=True)
