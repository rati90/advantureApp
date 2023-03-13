import os
from dotenv import load_dotenv, find_dotenv
from pydantic import EmailStr

load_dotenv(find_dotenv())

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URL")



API_V1_STR: str = "/api/v1"
FIRST_SUPERUSER: EmailStr
FIRST_SUPERUSER_PASSWORD: str