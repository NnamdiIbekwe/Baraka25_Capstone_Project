from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import logging
from fastapi.security import OAuth2PasswordRequestForm

from app.api.depends import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user import UserService
from app.core.security import verify_password, create_access_token
from app.schemas.auth import Token



router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/signup", response_model=UserRead,  status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = UserService.get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    try:
        user = UserService.create_user(db, user_in)
        logger.debug(f"User created with email: {user.email}")
        return user
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserService.get_user_by_email(db, email=form_data.username)
    if not user:
        logger.debug(f"Login failed for email: {form_data.username} - user not found")
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    
    if not verify_password(form_data.password, user.hashed_password):
        logger.debug(f"Login failed for email: {form_data.username} - incorrect password")
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    
    access_token = create_access_token(data={"sub":str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"} 