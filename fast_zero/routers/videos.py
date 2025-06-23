from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from http import HTTPStatus
from typing import List

from fast_zero.database import get_session
from fast_zero.models import Video
from fast_zero.schemas import Video, VideoCreate

router = APIRouter(prefix="/videos", tags=["videos"])


@router.get("/", response_model=List[Video])
def list_videos(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    return session.scalars(
        select(Video).order_by(Video.order_index).offset(skip).limit(limit)
    ).all()


@router.post("/", status_code=HTTPStatus.CREATED, response_model=Video)
def create_video(
    video_in: VideoCreate, session: Session = Depends(get_session)
):
    db_video = Video(**video_in.model_dump())
    session.add(db_video)
    session.commit()
    session.refresh(db_video)
    return db_video


@router.get("/{video_id}", response_model=Video)
def get_video(video_id: int, session: Session = Depends(get_session)):
    db_video = session.scalar(select(Video).where(Video.id == video_id))
    if not db_video:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Video not found")
    return db_video