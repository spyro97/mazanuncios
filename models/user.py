from pydantic import BaseModel
from fastapi import Query
import enum

class Role(str, enum.Enum):
    admin = "admin"
    normal_user = "normal_user"
    premium_user = "premium_user"

class User(BaseModel):
    username : str
    password : str
    email : str = Query(..., regex="(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    role: Role
    
class UserResponse(BaseModel):
    id_user : int
    username : str
    password : str
    email : str = Query(..., regex="(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    role: Role