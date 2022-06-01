import uvicorn
from fastapi import Body, APIRouter
from . import auth_alg

# import router

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from fastapi.security import HTTPBasicCredentials

from . import crud, models, schemas
from .database import SessionLocal, engine


router = APIRouter()


@router.get("/", tags=["greatings"])
async def hello():
	return {"hello": "World"}
    







models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users/me/", response_model=schemas.User)
def read_users_me(token: schemas.User = Depends(auth_alg.get_current_user), db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=token)
    if user is None:
        raise credentials_exception
    return user
    # return current_user


# @router.get("/users/me")
# def read_current_user(credentials: HTTPBasicCredentials = Depends(auth_alg.get_current_username), db: Session = Depends(get_db)):
#     # db_user = crud.get_user_by_email(db, email=credentials.email)
#     return {"email": credentials.email, "password": credentials.password}


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # user.password = hash_algs.get_password_hash(user.password)
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# @router.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @router.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
