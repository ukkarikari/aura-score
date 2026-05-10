import json

from sqladmin import ModelView
from sqlalchemy import Column, DateTime, Integer, String, func

from db.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.timezone("America/Sao_Paulo", func.now()),
        nullable=False,
    )


class UserAdmin(ModelView, model=User):
    column_list = [  # pyright: ignore[reportAssignmentType]
        User.id,
        User.username,
        User.password_hash,
        User.created_at,
    ]
