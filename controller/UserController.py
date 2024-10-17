import json

from fastapi import APIRouter, Request
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from db.postgresql.postgresql import db_instance
from models.UserModel import User, AccessToken
from models.UserModel import get_expiration_date, generate_token

from repository.RedisRepository import RedisRepository
from repository.UserRepository import UserRepository
from schemas.UserSchema import UserCreate, UserRead
from utils.password import get_password_hash
from uuid import UUID

router = APIRouter(
    prefix="/user",
    tags=["user"],

)

async def get_user_repository(rep: str = "UserRepository"):
    async for rep in db_instance.get_repository(rep):
        yield rep



@router.post("/register", status_code=HTTP_201_CREATED, response_model=UserRead)
async def register(
        user_create: UserCreate,
        repository: UserRepository = Depends(get_user_repository),
) -> User:
    password = get_password_hash(user_create.password)
    user = User(
        **user_create.dict(exclude={"password"}), password=password
    )
    try:
        user = await repository.create(user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )
    return user

@router.post("/token")
async def create_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    user_repository: UserRepository = Depends(get_user_repository),
):
    redis_repository: RedisRepository = RedisRepository(request.app)
    email = form_data.username
    password = form_data.password
    user = await user_repository.authenticate(email, password)
    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    token = generate_token()
    access_token: dict = {
        "access_token": token,
        "token_type": "bearer",
    }

    if not redis_repository.get(token):
        redis_repository.set(token, str(user.id), expire_second=86400)
    return access_token

async def get_current_user(
        request: Request,
        token: str = Depends(OAuth2PasswordBearer(tokenUrl="/user/token")),
        user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    redis_repository: RedisRepository = RedisRepository(request.app)
    if token is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    user_id = UUID(redis_repository.get(token))
    user = await user_repository.get(user_id)
    return user