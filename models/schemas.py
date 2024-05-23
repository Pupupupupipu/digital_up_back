from pydantic import BaseModel
from enum import Enum

class User_create(BaseModel):
    login: str
    password: str

class User_patch(BaseModel):
    id: int
    new_name: str

