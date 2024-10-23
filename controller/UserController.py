import json

from fastapi import APIRouter, Request
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, APIKeyCookie
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from db.postgresql.postgresql import db_instance
from models.UserModel import User
from models.UserModel import get_expiration_date, generate_token
from repository.AccessTokenRepository import AccessTokenRepository

from entites.AccessToken import AccessToken
from repository.RedisRepository import RedisRepository
from repository.UserRepository import UserRepository
from schemas.UserSchema import UserCreate, UserRead, UserUpdate
from utils.password import get_password_hash
from uuid import UUID
from fastapi import Depends, FastAPI, Form, HTTPException, Response, status
from config import settings

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
    token_repository: AccessTokenRepository = AccessTokenRepository(request.app)
    email = form_data.username
    password = form_data.password
    user = await user_repository.authenticate(email, password)
    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    token = AccessToken().generate_token()

    if not token_repository.get_user(token):
        token_repository.create_token(token, user.id)
    return token.get_access_token()

async def get_current_user(
        request: Request,
        token: AccessToken = Depends(APIKeyCookie(name=settings.TOKEN_COOKIE_NAME)),
        user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    token_repository: AccessTokenRepository = AccessTokenRepository(request.app)

    user_id:UUID = token_repository.get_user(token)
    if user_id is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    user = await user_repository.get(user_id)
    return user

@router.post("/login")
async def login(
        request: Request,
        response: Response,
        email: str = Form(...),
        password: str = Form(...),
        user_repository: UserRepository = Depends(get_user_repository),
):
    cookie = request.cookies
    token_repository: AccessTokenRepository = AccessTokenRepository(request.app)
    user = await user_repository.authenticate(email, password)

    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    token = AccessToken().generate_token()

    token_repository.create_token(token, user.id)
    response.set_cookie(
        settings.TOKEN_COOKIE_NAME,
        str(token),
        max_age=token.expire_second,
        secure=True,
        httponly=True,
        samesite="lax",
    )


@router.patch("/me", response_model=UserRead)
async def update(
    user_update: UserUpdate,
    user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
):
    user_update_dict = user_update.dict(exclude_unset=True)
    for key, value in user_update_dict.items():
        setattr(user, key, value)

    return await user_repository.create(user)
