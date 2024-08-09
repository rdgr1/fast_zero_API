from datetime import datetime, timedelta

from jwt import encode
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo
from fastapi.security import OAuth2PasswordBearer(tokenUrl="token")

pwd_context = PasswordHash.recommended()

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


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):