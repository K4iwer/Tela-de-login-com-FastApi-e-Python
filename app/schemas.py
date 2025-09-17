from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    password: str

class UserSchemaWithoutId(BaseModel):
    username: str
    email: str
    password: str

class RegistroCreate(BaseModel):
    pass

class RegistroInserted(BaseModel):
    id: str
    username: str
    email: str

class UserLoginSchema(BaseModel):
    username: str
    password: str
