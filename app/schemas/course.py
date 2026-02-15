from pydantic import BaseModel, EmailStr, Field, ConfigDict
import uuid

class CourseBase(BaseModel):
    title: str
    code: str
    capacity: int = Field(..., gt=0)
    
class CourseCreate(CourseBase):
    is_active: bool = True

class CourseRead(CourseBase):
    id: uuid.UUID
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class CourseUpdate(BaseModel):
    title: str | None = None
    code: str | None = None
    capacity: int | None = Field(None, gt=0)
    is_active: bool | None = None


    