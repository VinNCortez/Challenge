from datetime import datetime, timedelta
from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from google.api_core.exceptions import AlreadyExists
from google.cloud.firestore_v1 import Client
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette import status


from dependencies import get_database
from settings import settings

router = APIRouter(prefix="/auth-user")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth-user/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthUser(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    active: Union[bool, None] = True


class AuthUserInDb(AuthUser):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


def get_user(database: Client, username: str):
    auth_user = database.collection("auth_user").document(username).get()
    if auth_user.exists:
        return AuthUserInDb(**auth_user.to_dict())


def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)


def authenticate_auth_user(database: Client, username: str, password: str):
    user = get_user(database, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_auth_user(
        token: str = Depends(oauth2_scheme), database: Client = Depends(get_database)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(database, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_auth_user(
        current_user: AuthUser = Depends(get_current_auth_user)):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


@router.post("/login", response_model=Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        database: Client = Depends(get_database)
):
    user = authenticate_auth_user(database, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/", dependencies=[Depends(oauth2_scheme)], response_model=AuthUser)
async def auth_user_me(current_user: AuthUser = Depends(get_current_active_auth_user)):
    return current_user


@router.post("/")
async def create_auth_user(auth_user: AuthUserInDb, database: Client = Depends(get_database)):
    auth_user.password = pwd_context.hash(auth_user.password)
    try:
        database.collection("auth_user").document(auth_user.username).create(auth_user.dict())
    except AlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Esse usuário já existe"
        )
    return {"message": "success"}