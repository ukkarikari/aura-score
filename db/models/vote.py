import json

from sqladmin import ModelView
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import relationship

from db.database import Base


class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    voter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    voter = relationship("User", foreign_keys=[voter_id])
    target_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target = relationship("User", foreign_keys=[target_id])
    value = Column(Integer, nullable=False)
    reason = Column(Text)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.timezone("America/Sao_Paulo", func.now()),
        nullable=False,
    )


class VoteAdmin(ModelView, model=Vote):
    column_list = [  # pyright: ignore[reportAssignmentType]
        Vote.id,
        Vote.voter_id,
        Vote.target_id,
        Vote.voter,
        Vote.target,
        Vote.value,
        Vote.reason,
        Vote.created_at,
    ]
