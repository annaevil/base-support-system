from pydantic import (
    BaseModel,
    Field,
)
from uuid import UUID
from datetime import datetime


class VersionModel(BaseModel):
    """Версия API"""
    version: str = Field(default=None, title='Версия', description='Номер версии в виде X.Y[.Z]')


class TaskModel(BaseModel):
    header: str = Field(title='Заголовок обращения ', description='У меня не работает ...')
    description: str = Field(title='Описаине обращения ', description='Описаниея')


class TaskResponseModel(BaseModel):
    id: UUID = Field()
    header: str = Field()
    description: str = Field()
    created_at: datetime = Field()
    executor_id: UUID = Field()
    status: str = Field()
    user_id: UUID = Field()


class UpdateTaskModel(BaseModel):
    status: str = Field()
