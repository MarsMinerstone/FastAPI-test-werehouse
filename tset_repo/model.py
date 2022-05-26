from typing import TypeVar, Optional
from pydantic import BaseModel, Field, EmailStr


T = TypeVar('T')

# Model for User
class User(BaseModel):
	username : str = Field(default=None)
	fullname : str = Field(default=None)
	email : EmailStr = Field(default=None)
	hashed_password : str = Field(default=None)
	root : bool = Field(default=False)

# Model for Updating User
class UpdateUser(BaseModel):
	username : Optional[str]
	fullname : Optional[str]
	email : Optional[EmailStr]
	root : Optional[bool]