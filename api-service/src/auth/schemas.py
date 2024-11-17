import uuid
from typing import Optional
from uuid import UUID

from fastapi_users import schemas


class UserUpdate(schemas.BaseUserUpdate):
    pass


class UserCreate(schemas.BaseUserCreate):
    email: str
    password: str
    role_id: Optional[str] = 'adebb055-9b61-4f59-b1f2-824d007ca6a3'
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserRead(schemas.BaseUser):
    id: UUID
    email: str
    role_id: UUID
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True
