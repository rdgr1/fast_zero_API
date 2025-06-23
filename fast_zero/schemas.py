# fast_zero/schemas.py

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

# Payload extraído do JWT
class TokenData(BaseModel):
    sub: Optional[str] = Field(None, alias="username")
    exp: Optional[datetime] = None

# --- Auth ---
class Token(BaseModel):
    access_token: str
    token_type: str

# --- Users ---
class UserSchema(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class UserList(BaseModel):
    users: List[UserPublic]

class Message(BaseModel):
    message: str

# --- Videos ---
class VideoBase(BaseModel):
    youtube_id: str
    title: str
    description: str
    order_index: int

class VideoCreate(VideoBase):
    pass

class Video(VideoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# --- Challenges ---
class ChallengeBase(BaseModel):
    video_id: int
    prompt: str
    type: str  # e.g. "CODING" / "MCQ"

class ChallengeCreate(ChallengeBase):
    pass

class Challenge(ChallengeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# --- Responses ---
class ResponseBase(BaseModel):
    challenge_id: int
    code: str

class ResponseCreate(ResponseBase):
    pass

class Response(ResponseBase):
    id: int
    user_id: int
    passed: bool
    submitted_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Progress ---
class ProgressBase(BaseModel):
    video_id: int
    status: str  # NOT_STARTED / IN_PROGRESS / COMPLETED

class ProgressCreate(ProgressBase):
    pass

class Progress(ProgressBase):
    user_id: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)