from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from http import HTTPStatus

from fast_zero.database import get_session
from fast_zero.models import Response, Challenge
from fast_zero.schemas import ResponseCreate, Response as ResponseOut

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.post("/{challenge_id}/submit", response_model=ResponseOut)
def submit_challenge(
    challenge_id: int,
    resp_in: ResponseCreate,
    session: Session = Depends(get_session)
):
    # verifica existência do challenge
    ch = session.scalar(select(Challenge).where(Challenge.id == challenge_id))
    if not ch:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Challenge not found")

    # Aqui você teria a lógica de sandbox para avaliar o código
    passed = False
    # ... executar resp_in.code e definir passed True/False ...

    db_resp = Response(
        user_id=resp_in.user_id,
        challenge_id=challenge_id,
        code=resp_in.code,
        passed=passed
    )
    session.add(db_resp)
    session.commit()
    session.refresh(db_resp)
    return db_resp