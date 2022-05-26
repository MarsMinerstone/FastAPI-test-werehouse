from datetime import datetime, timedelta
from typing import Union, List

from starlette.responses import JSONResponse

from model import User, UpdateUser
from config import database

from fastapi import Depends, FastAPI, HTTPException, status, Body, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

# Creatined Keys and Algorithms
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# Entered Pasword werifing with Hashed password in db
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Creating Hash of pasword
def get_password_hash(password):
    return pwd_context.hash(password)

# getting user from db
async def get_user(username: str):
    if (username := await database["user"].find_one({"username": username})) is not None:
        return UserInDB(**username)
    else:
        return None

# authenticating user by two upper functions
async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

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

# Getting current user by token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Checking user by full access
async def get_current_root_user(current_user: User = Depends(get_current_user)):
    if not current_user.root:
        raise HTTPException(status_code=400, detail="permission denied")
    return current_user

# Logging in to get JWT token
@app.post("/token", response_model=Token, tags=["login"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(form_data.username),
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Create New User
@app.post("/", response_description="Add new user", response_model=User, dependencies=[Depends(jwtBearer())], tags=["CRUD"])
async def create_user(user: User = Body(...), current_user: User = Depends(get_current_root_user)):
    info = await get_user(user.username)
    if info is None:
        if len(user.hashed_password) < 8:
            raise HTTPException(status_code=400, detail="Passwor must be more than 8 charachters")
        user.hashed_password = get_password_hash(user.hashed_password)
        user = jsonable_encoder(user)
        new_user = await database["user"].insert_one(user)
        return user
    else:
        raise HTTPException(status_code=400, detail="This user already exist")

# Get list of users
@app.get("/", response_description="List all users", response_model=List[User], dependencies=[Depends(jwtBearer())], tags=["CRUD"])
async def list_users(current_user: User = Depends(get_current_user)):
    users = await database["user"].find().to_list(1000)
    return users

# get one user by Username
@app.get("/{username}", response_description="Get a single user", response_model=User, dependencies=[Depends(jwtBearer())], tags=["CRUD"])
async def show_user(username: str, current_user: User = Depends(get_current_user)):
    if (user := await database["user"].find_one({"username": username})) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"User {username} not found")

# Update user
@app.put("/{username}", response_description="Update a user", response_model=User, dependencies=[Depends(jwtBearer())], tags=["CRUD"])
async def update_user(username: str, user: UpdateUser = Body(...), current_user: User = Depends(get_current_root_user)):
    user = {k: v for k, v in user.dict().items() if v is not None}

    if len(user) >= 1:
        update_result = await database["user"].update_one({"username": username}, {"$set": user})

        if update_result.modified_count == 1:
            if (
                updated_user := await database["user"].find_one({"username": username})
            ) is not None:
                return updated_user

    existing_user = await get_user(username)
    if existing_user is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f"User {username} not found")

# Delete user
@app.delete("/{username}", response_description="Delete a user", dependencies=[Depends(jwtBearer())], tags=["CRUD"])
async def delete_user(username: str, current_user: User = Depends(get_current_root_user)):
    delete_result = await database["user"].delete_one({"username": username})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"User {username} not found")