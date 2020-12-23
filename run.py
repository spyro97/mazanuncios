from fastapi import FastAPI, Depends, HTTPException
from routes.v1 import app_v1
from utils.db_object import db
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.requests import Request
from fastapi.security import OAuth2PasswordRequestForm
from utils.security import authenticate_user, create_jwt_token, check_jwt_token
from models.jwt_user import JWTUser
from utils.const import (
    TOKEN_INVALID_CREDENTIALS_MSG,
    REDIS_URL,
    TOKEN_DESCRIPTION,
    TOKEN_SUMMARY
)
import utils.redis_object as re
import aioredis
from datetime import datetime

#----------Instanciar APP------------#
app = FastAPI()
app = FastAPI(title='Mazanuncios API Documentation', description='Oficial api for mazanuncios.', version="1.0.0")


#----------Agregar endpoints por medio de include_router------------#
app.include_router(
    app_v1,
    prefix="/v1",
    dependencies=[Depends(check_jwt_token)]
)


#----------Conectar y desconectar la base de datos------------#
@app.on_event("startup")
async def connect_db():
    await db.connect()
    re.redis = await aioredis.create_redis_pool(REDIS_URL)


@app.on_event("shutdown")
async def disconnect_db():
    await db.disconnect()
    re.redis.close()
    await re.redis.wait_closed()
    


#----------Revisar si esta activa la api------------#
@app.get("/", tags=["Health Checker"])
async def health_check():
    return {"status":"online"}


#----------Obtener Token------------#
@app.post("/token", description=TOKEN_DESCRIPTION, summary=TOKEN_SUMMARY, tags=["Token"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    jwt_user_dict = {"username": form_data.username, "password": form_data.password}
    jwt_user = JWTUser(**jwt_user_dict)
    user = await authenticate_user(jwt_user)

    if user is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail=TOKEN_INVALID_CREDENTIALS_MSG
        )
    jwt_token = create_jwt_token(user)
    return {"access_token": jwt_token}


#----------Middleware------------#
@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()

    response = await call_next(request)

    # modify response
    execution_time = (datetime.utcnow() - start_time).microseconds
    response.headers["x-execution-time"] = str(execution_time)
    return response

