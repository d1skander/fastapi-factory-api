from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jwt.exceptions import InvalidTokenError

from pydantic import BaseModel

from dotenv import load_dotenv


import jwt
import os


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
MINUTE = str(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ACCESS_TOKEN_EXPIRE_MINUTES = int(MINUTE)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    verification_id: str | None = None