from dataclasses import dataclass
from typing import List, Union, Dict

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from google.api_core.exceptions import AlreadyExists, NotFound
from pydantic import BaseModel
import requests
from starlette import status
from google.cloud.firestore_v1.client import Client

from dependencies import get_database
from routers.auth_user import oauth2_scheme

GITHUB_API_URL = "https://api.github.com/search/users"

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Usuário não encontrado"
)


class Endereco(BaseModel):
    cep: int
    codigo_ibge: int
    uf: str
    cidade: str
    logradouro: str


class User(BaseModel):
    id: int
    nome: str
    idade: int
    endereco: Endereco
    nome_github: str

    def __str__(self):
        return f"user: {self.nome} - {self.idade}"


class GithubInfo(BaseModel):
    id: int
    avatar_url: str
    html_url: str
    repositorios: List[Union[dict, None]] = None


async def resolve_github(user: User, database: Client):
    users_response = requests.get(GITHUB_API_URL, params={"q": user.nome_github}).json()
    if users_response["total_count"] == 1:
        github_user = users_response["items"][0]
        repos_response = requests.get(github_user["repos_url"]).json()
        github_info = GithubInfo(**github_user)
        github_info.repositorios = repos_response

        database.collection("users").document(str(user.id)).update({"github": github_info.dict()})


router = APIRouter(prefix="/user", dependencies=[Depends(oauth2_scheme)])


@router.get("/", response_model=List[User])
async def index(database: Client = Depends(get_database)):
    data = database.collection("users").get()
    result = [user.to_dict() for user in data]
    return result


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, database: Client = Depends(get_database)):
    user = database.collection("users").document(str(user_id)).get()
    if not user.exists:
        raise UserNotFoundException
    return user.to_dict()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User, task: BackgroundTasks, database: Client = Depends(get_database)):
    try:
        database.collection("users").document(str(user.id)).create(user.dict())
    except AlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "invalid_inputs": [
                    {"name": "id",
                     "description": "O id informado já existe"
                     },
                ]}
        )
    task.add_task(resolve_github, user, database)

    return {"message": "sucesso"}


@router.put("/{user_id}")
async def update_user(user_id: int, user: User, database: Client = Depends(get_database)):
    try:
        database.collection("users").document(str(user_id)).update(user.dict())
    except NotFound:
        raise UserNotFoundException
    return {"message": "sucesso"}


@router.delete("/{user_id}")
async def delete_user(user_id: int, database: Client = Depends(get_database)):
    user = database.collection("users").document(str(user_id))
    if not user.get().exists:
        raise UserNotFoundException
    user.delete()
    return {"message": "sucesso"}


@router.post("/update-github-info/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_github_info(user_id: int, task: BackgroundTasks, database: Client = Depends(get_database)):
    user = database.collection("users").document(str(user_id)).get()
    if not user.exists:
        raise UserNotFoundException
    user = User(**user.to_dict())
    task.add_task(resolve_github(user, database))
    return {"message": "sucesso"}