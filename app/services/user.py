from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserRole, UserUpdate
from sqlalchemy.orm import Session
from app.core.security import get_password_hash



def _safe_hash(password: str) -> str:
    if len(password.encode('utf-8')) > 72:
        raise ValueError("Password is too long. Maximum length is 72 bytes.")
    return get_password_hash(password)

class UserService:
    
    @staticmethod
    def create_user(db: Session, user_in: UserCreate) -> User:
        hashed_password = _safe_hash(user_in.password)
        db_user = User(
            name=user_in.name,
            email=user_in.email,
            hashed_password=hashed_password,
            role=user_in.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def update_user(db: Session, user: User, user_in: UserUpdate) -> User:
        for field, value in user_in.model_dump(exclude_unset=True).items():
            if field == "password":
                setattr(user, "hashed_password", _safe_hash(value))
            else:
                setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def delete_user(db: Session, user: User) -> None:
        db.delete(user)
        db.commit()