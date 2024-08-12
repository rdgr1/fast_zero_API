from datetime import datetime, timedelta
from http import HTTPStatus

from jwt import encode, decode, DecodeError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from sqlalchemy import select
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fast_zero.database import get_session
from fast_zero.models import  User
from fast_zero.schema import TokenData

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = 'you-secret-key'
ALGORITHM = 'HS256'
ACESS_TOKEN_EXPIRES_MINUTES = 30


def get_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_acess_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACESS_TOKEN_EXPIRES_MINUTES
    )

    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def get_current_user():
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),

    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validated credentials'
        headers={'WWW.Authenticate':'Bearer'}
    )
    try:
        payload = decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        username: str