import uuid
from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base




class Course(Base):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4,  primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    capacity = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    enrollments = relationship("Enrollment", back_populates="course")