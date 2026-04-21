import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.shared import UserRole


class UserCreate(BaseModel):
    email: str
    name: str
    password: str
    role: UserRole


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    name: str
    role: UserRole
    active: bool
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: str
    password: str
