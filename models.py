from typing import TypeVar, Optional
from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
	username: str = Field(default=None)
	fullname: str = Field(default=None)
	email: EmailStr = Field(default=None)
	hashed_password: str = Field(default=None)
	employe: bool = Field(default=False)

# Model for Updating User
class UpdateUser(BaseModel):
	username: Optional[str]
	fullname: Optional[str]
	email: Optional[EmailStr]
	root: Optional[bool]


class Werehouse(BaseModel):
	w_name: str = Field(default=None)
	product_count: int = Field(default=None)


class Token(BaseModel):
    access_token: str
    token_type: str


class UserInDB(User):
    hashed_password: str