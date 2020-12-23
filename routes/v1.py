from aioredis.commands import string
from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from models.user import User, UserResponse
from utils.db_functions import db_insert_user, retrieve_user, delete_users
from utils.security import get_hashed_password
import utils.redis_object as re
import pickle

app_v1 = APIRouter()


@app_v1.post("/user", status_code=HTTP_201_CREATED, tags=["User"])
async def post_user(user: User):
    user.password = get_hashed_password(user.password)
    create_user = await db_insert_user(user)
    if create_user:
        return {"data": user, "message": "success"}
    else:
        raise HTTPException(status_code=400, detail="Ocurrio un problema al crear el usuario.")
    

@app_v1.get("/user/{username}", status_code=HTTP_200_OK, tags=["User"])
async def get_user_by_pk(username: str):
    result = await re.redis.get(username)
    if result:
        result_user = pickle.loads(result)
        return result_user
    else:
        user = await retrieve_user(username)
        if user:
            result_user = UserResponse(**user)
            await re.redis.set(username, pickle.dumps(result_user))
            return {"data": result_user}
    raise HTTPException(status_code=400, detail="Ocurrio un error al obtener al usuario.")
    
@app_v1.delete("/users",status_code=HTTP_200_OK, tags=["User"])
async def delete_all_users():
    deleted_users = await delete_users()
    if deleted_users:
        return {"message": "Todos los usuarios fueron eliminados"}
    else:
        return {"message": "Ocurrio un error al eliminar los usuario."}
