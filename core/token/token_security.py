from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer

from dotenv import load_dotenv


import jwt
import os


load_dotenv()


oauth2_sheme = OAuth2PasswordBearer(tokenUrl="/workers/auth")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("OAUTH_SECRET_KEY"), algorithm=os.getenv("OAUTH_ALGORITHM"))
    return encoded_jwt