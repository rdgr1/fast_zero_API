from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import UserSchema, UserPublic, UserList, Message
from fast_zero.security import get_password, get_current_user

router = APIRouter(prefix="/users", tags=["users"])

# Criar um novo usuário
@router.post("/", response_model=UserPublic)
def create_user(user_in: UserSchema, session: Session = Depends(get_session)):
    # Verifica se email ou username já existe
    existente = session.scalar(
        select(User).where(
            (User.email == user_in.email) |
            (User.username == user_in.username)
        )
    )
    if existente:
        raise HTTPException(HTTPStatus.CONFLICT, "Email ou usuário já cadastrado")
    # Cria instância de User com senha criptografada
    novo = User(
        username=user_in.username,
        email=user_in.email,
        password=get_password(user_in.password)
    )
    session.add(novo)
    session.commit()
    session.refresh(novo)
    return novo

# Listar todos os usuários (precisa de autenticação)
@router.get("/", response_model=UserList)
def list_users(
    session: Session = Depends(get_session),
    current: User = Depends(get_current_user)
):
    usuarios = session.scalars(select(User)).all()
    return UserList(users=usuarios)

# Obter usuário por ID (precisa de autenticação)
@router.get("/{user_id}", response_model=UserPublic)
def get_user(
    user_id: int,
    session: Session = Depends(get_session),
    current: User = Depends(get_current_user)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Usuário não encontrado")
    return user

# Deletar usuário por ID (precisa de autenticação)
@router.delete("/{user_id}", response_model=Message)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current: User = Depends(get_current_user)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Usuário não encontrado")
    session.delete(user)
    session.commit()
    return Message(message="Usuário deletado")
