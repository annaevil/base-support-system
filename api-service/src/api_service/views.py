import uvicorn
from database.models import User
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .schemas import (
    VersionModel
)

from auth.schemas import UserCreate, UserRead, UserUpdate
from auth.base_config import auth_backend, current_active_user, fastapi_users

origins = [
    "*"
]

app = FastAPI(
    title='API Service',
    version='0.1',
    description="SympfonicMasks API Service",
    root_path="/api/v1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

fastapi_users.current_user(current_active_user)


@app.get(
    '/version',
    description='Возвращает версию API',
    responses={
        200: {'description': 'Версия API', 'content': {'application/json': {'example': '0.1.0'}}}
    }
)
async def get_version() -> VersionModel:
    return VersionModel(
        version=app.version
    )


@app.get("/protected-route")
def protected_route(user: User = Depends(current_active_user)):
    return f"Hello, {user.email}. You are authenticated with a cookie or a JWT."


@app.get("/protected-route-only-jwt")
def protected_route(user: User = Depends(current_active_user)):
    return f"Hello, {user.email}. You are authenticated with a JWT."


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8020)
