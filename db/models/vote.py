import json

from sqladmin import ModelView
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func

from db.database import Base


class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    voter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    value = Column(Integer, nullable=False)
    reason = Column(Text)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class VoteAdmin(ModelView, model=Vote):
    column_list = [  # pyright: ignore[reportAssignmentType]
        Vote.id,
        Vote.voter_id,
        Vote.target_id,
        Vote.value,
        Vote.reason,
        Vote.created_at,
    ]
