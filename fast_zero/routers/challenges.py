from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from http import HTTPStatus
from typing import List

from fast_zero.database import get_session
from fast_zero.models import Challenge
from fast_zero.schemas import Challenge, ChallengeCreate

router = APIRouter(prefix="/challenges", tags=["challenges"])


@router.get("/", response_model=List[Challenge])
def list_challenges(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    return session.scalars(
        select(Challenge).offset(skip).limit(limit)
    ).all()


@router.get("/video/{video_id}", response_model=List[Challenge])
def get_challenges_for_video(
    video_id: int, session: Session = Depends(get_session)
):
    return session.scalars(
        select(Challenge).where(Challenge.video_id == video_id)
    ).all()


@router.post("/", status_code=HTTPStatus.CREATED, response_model=Challenge)
def create_challenge(
    ch_in: ChallengeCreate, session: Session = Depends(get_session)
):
    db_ch = Challenge(**ch_in.model_dump())
    session.add(db_ch)
    session.commit()
    session.refresh(db_ch)
    return db_ch