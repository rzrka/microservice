from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    debug: bool = False
    DB_HOST:str
    DB_PORT:str
    DB_NAME:str
    DB_USER:str
    DB_PASS:str
    DB_SCHEMA:str
    TOKEN_COOKIE_NAME:str = "token"
    CSRF_TOKEN_SECRET:str = "__CHANGE_THIS_WITH_YOUR_OWN_SECRET_VALUE__"
    API_TOKEN:str = "secret_api_token"
    class Config:
        env_file = ".env"


settings = Settings()