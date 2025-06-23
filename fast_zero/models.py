from datetime import datetime
from sqlalchemy import (
    Integer, String, Boolean, DateTime, ForeignKey, Enum as SAEnum, Text
)
from sqlalchemy.orm import Mapped, mapped_column, registry
import enum

mapper_registry = registry()
Base = mapper_registry.generate_base()

class RoleEnum(str, enum.Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    ADMIN   = "ADMIN"

@mapper_registry.mapped_as_dataclass
class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, init=False)
    username: Mapped[str]   = mapped_column(String, unique=True, index=True)
    email: Mapped[str]      = mapped_column(String, unique=True, index=True)
    password: Mapped[str]   = mapped_column(String)
    role: Mapped[RoleEnum]  = mapped_column(SAEnum(RoleEnum), default=RoleEnum.STUDENT)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, init=False)

# Video entity
@mapper_registry.mapped_as_dataclass
class Video:
    __tablename__ = "videos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, init=False)
    youtube_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    order_index: Mapped[int] = mapped_column(Integer)

# Challenge entity
@mapper_registry.mapped_as_dataclass
class Challenge:
    __tablename__ = "challenges"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, init=False)
    video_id: Mapped[int] = mapped_column(Integer, ForeignKey("videos.id"))
    prompt: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)  # e.g. "CODING" / "MCQ"

# Response entity
@mapper_registry.mapped_as_dataclass
class Response:
    __tablename__ = "responses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, init=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    challenge_id: Mapped[int] = mapped_column(Integer, ForeignKey("challenges.id"))
    code: Mapped[str] = mapped_column(Text)
    passed: Mapped[bool] = mapped_column(Boolean, default=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, init=False)

# Progress entity
@mapper_registry.mapped_as_dataclass
class Progress:
    __tablename__ = "progress"
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    video_id: Mapped[int] = mapped_column(Integer, ForeignKey("videos.id"), primary_key=True)
    status: Mapped[str] = mapped_column(String)  # NOT_STARTED / IN_PROGRESS / COMPLETED
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, init=False)