from datetime import datetime

import uvicorn
from database.models import User, Task
from database.db import get_async_session
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update

from .schemas import (
    VersionModel,
    TaskModel,
    TaskResponseModel,
    UpdateTaskModel
)
from .utils import check_user_role
from typing import List

from auth.schemas import UserCreate, UserRead, UserUpdate
from auth.base_config import auth_backend, current_active_user, fastapi_users

origins = [
    "http://localhost:8084"
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
    return f"Hello, {user.role_id}. You are authenticated with a cookie or a JWT."


@app.post(
    "/task/create-task",
    tags=['task'],
    description='Метод для создания задчи пользователем',

)
async def create_task(
        task: TaskModel,
        user: User = Depends(current_active_user),
        session: Session = Depends(get_async_session)

) -> TaskResponseModel:
    if await check_user_role(user.role_id) != 'user':
        raise HTTPException(status_code=404, detail="only user")

    stmt = insert(Task).returning(Task).values(
        header=task.header,
        description=task.description,
        status='new',
        created_at=datetime.utcnow(),
        user_id=user.id,
    )

    result = await session.execute(stmt)
    created_task = result.scalar_one()

    await session.commit()

    return created_task


@app.get(
    "/task/load_tasks",
    tags=['task'],
    description='Загружает задачи',
)
async def load_tasks(
        user: User = Depends(current_active_user),
        session: Session = Depends(get_async_session)
) -> List[TaskResponseModel]:
    if await check_user_role(user.role_id) not in ['tolk_support', 'tech_support']:
        raise HTTPException(status_code=404, detail="Only support can load tasks")

    stmt = select(Task)
    result = await session.execute(stmt)
    tasks = result.scalars().all()

    return [TaskResponseModel(
        id=task.id,
        header=task.header,
        description=task.description,
        created_at=task.created_at.isoformat(),
        user_id=task.user_id,
        status=task.status,
        executor_id=task.executor_id,
    ) for task in tasks]


@app.patch(
    "/task/{task_id}",
    tags=['task'],
    description='Изменяет статус задачи'
)
async def update_task(
        task_id: str,
        task_update: UpdateTaskModel,
        user: User = Depends(current_active_user),
        session: Session = Depends(get_async_session)
) -> TaskResponseModel:
    if await check_user_role(user.role_id) not in ['tolk_support', 'tech_support']:
        raise HTTPException(status_code=404, detail="Only support can load tasks")

    stmt = (update(Task).
            where(Task.id == task_id).
            values(status=task_update.status).
            returning(Task))
    result = await session.execute(stmt)
    await session.commit()

    updated_task = result.scalar_one()

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8020)
