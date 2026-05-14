# from fastapi import Depends, HTTPException
# from sqlalchemy.orm import Session
# import uuid

# from app.db.session import SessionLocal
# from app.models.user import User
# from app.core.security import decode_access_token
# from fastapi.security import OAuth2PasswordBearer
# from typing import List
# from app.schemas.user import UserRole



# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")  

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def get_current_user(
#     token: str = Depends(oauth2_scheme), 
#     db: Session = Depends(get_db)
# ):
#     data = decode_access_token(token)
#     if not data:
#         raise HTTPException(
#             status_code=401, detail="Invalid authentication credentials")
    
#     sub = data.get("sub")
#     if not sub:
#         raise HTTPException(
#             status_code=401, detail="Invalid token payload"
#         )
#     try:
#         user_id = uuid.UUID(sub)
#     except (ValueError, TypeError):
#         raise HTTPException(
#             status_code=401, detail="Invalid token payload")

#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(
#             status_code=401, detail="User not found")
#     return user

# def get_current_active_user(
#     current_user: User = Depends(get_current_user)
# ):
#     if not current_user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# def RoleChecker(required_role: List[UserRole]):
#     def role_checker(current_user: User = Depends(get_current_active_user)):
#         print(f"Checking role for user {current_user.email}: required {required_role}, actual {current_user.role}")
#         # Ensure type-safe comparison for Enum
#         user_role = current_user.role
#         if isinstance(user_role, str):
#             try:
#                 user_role = UserRole(user_role)
#             except ValueError:
#                 raise HTTPException(status_code=403, detail="Invalid user role")
#         if user_role not in required_role:
#             raise HTTPException(status_code=403, detail="Not enough permissions")
#         return current_user
#     return role_checkerxception(status_code=403, detail="Not enough permissions")
#         return current_user
#     return role_checker

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from typing import List
from app.schemas.user import UserRole


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    data = decode_access_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    sub = data.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    try:
        user_id = uuid.UUID(sub)
    except (ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def RoleChecker(required_roles: List[UserRole]):
    def role_checker(current_user: User = Depends(get_current_active_user)):
        print(f"User role: '{current_user.role}' | Type: {type(current_user.role)}")
        print(f"Required roles: {required_roles} | Type: {type(required_roles[0])}")
        if current_user.role not in required_roles:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return current_user
    return role_checker