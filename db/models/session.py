from logging import StringTemplateStyle

from sqladmin import ModelView
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)

    session_token = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    user = relationship("User")


class SessionAdmin(ModelView, model=Session):
    column_list = [Session.id, Session.session_token, Session.user_id, Session.user]  # pyright: ignore[reportAssignmentType]
