# from typing import TypeVar, Optional
# from pydantic import BaseModel, Field, EmailStr

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_employe = Column(Boolean, default=False)



class Werehouse(Base):
    __tablename__ = "werehouse"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    count = Column(Integer, index=True)


















# class User(BaseModel):
# 	username: str = Field(default=None)
# 	fullname: str = Field(default=None)
# 	email: EmailStr = Field(default=None)
# 	hashed_password: str = Field(default=None)
# 	employe: bool = Field(default=False)

# # Model for Updating User
# class UpdateUser(BaseModel):
# 	username: Optional[str]
# 	fullname: Optional[str]
# 	email: Optional[EmailStr]
# 	root: Optional[bool]


# class Werehouse(BaseModel):
# 	w_name: str = Field(default=None)
# 	product_count: int = Field(default=None)


# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class UserInDB(User):
#     hashed_password: str