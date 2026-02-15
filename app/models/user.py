from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Enum as SqlEnum
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.schemas.user import UserRole



class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4,  primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(SqlEnum(UserRole, name="user_role"), nullable=False, default=UserRole.STUDENT)
    is_active = Column(Boolean, nullable=False, default=True)

    enrollments = relationship("Enrollment", back_populates="user")