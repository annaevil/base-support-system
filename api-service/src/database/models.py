import uuid

from sqlalchemy import (
    String,
    TIMESTAMP,
    Boolean,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from uuid import UUID
from .db import Base
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from datetime import datetime


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True)
    email: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(30), nullable=True)
    registered_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    hashed_password: Mapped[str] = mapped_column(String(1024), nullable=False)
    is_active: Mapped[str] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[str] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[str] = mapped_column(Boolean, default=False, nullable=False)
