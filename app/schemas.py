from pydantic import BaseModel
from typing import List, Optional 

class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    password: str

class RegistroCreate(UserSchema):
    pass

class UserLoginSchema(BaseModel):
    username: str
    password: str
