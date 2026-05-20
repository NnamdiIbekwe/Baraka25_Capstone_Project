from pydantic import BaseModel, ConfigDict
import uuid

class EnrollmentBase(BaseModel):
    user_id: uuid.UUID
    course_id: uuid.UUID 
      

class EnrollmentCreate(EnrollmentBase):
    pass    

class EnrollmentRead(EnrollmentBase):
    id: uuid.UUID
    created_at: str
    updated_at: str
    # user_name: str
    # course_title: str

    model_config = ConfigDict(from_attributes=True)
        
class EnrollmentUpdate(BaseModel):
    user_id: uuid.UUID | None = None
    course_id: uuid.UUID | None = None

    model_config = ConfigDict(from_attributes=True)