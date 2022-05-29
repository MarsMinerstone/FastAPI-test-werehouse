from fastapi import Depends, HTTPException, status, Body, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from datetime import datetime, timedelta
from models import *
from typing import Union, List

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Creating JWT token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Class for JWT Bearer (JWT access)
class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error: bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_Error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code = 403, details="Invalid or Expired Token")
            return credentials.credentials
        else:
            raise HTTPException(status_code = 403, details="Invalid or Expired Token")

    def verify_jwt(self, jwtoken: str):
        isTokenValid: bool = False # flag
        payload = jwt.decode(jwtoken)
        if payload:
            isTokenValid = True
        return isTokenValid