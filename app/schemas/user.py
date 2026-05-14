from pydantic import BaseModel, EmailStr, ConfigDict
import uuid
from datetime import datetime

from app.models.user import UserRole


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole
    

class UserCreate(UserBase):
    password: str
    
class UserRead(UserBase):
    id: uuid.UUID
    updated_at: datetime | None = None
    created_at: datetime | None = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None

    model_config = ConfigDict(from_attributes=True)

