from typing import List, Union

from pydantic import BaseModel


class WerehouseBase(BaseModel):
    title: str
    count: Union[int, None] = None


class WerehouseCreate(WerehouseBase):
    pass


class Werehouse(WerehouseBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_employe: bool


    class Config:
        orm_mode = True
