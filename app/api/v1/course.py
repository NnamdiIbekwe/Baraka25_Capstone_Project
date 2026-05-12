from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.depends import get_db, get_current_active_user, RoleChecker
from app.schemas.user import UserRole
from app.schemas.course import CourseCreate, CourseRead
from app.services.course import CourseService
from app.schemas.enrollment import EnrollmentRead
from app.models.user import User


router = APIRouter()

@router.post("/", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(
    course_in: CourseCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(RoleChecker([UserRole.ADMIN])),
):
    # if current_user.role != "admin":
    #     raise HTTPException(status_code=403, detail="Not authorized to create courses")

    existing_course = CourseService.get_course_by_code(db, course_in.code)
    if existing_course:
        raise HTTPException(status_code=400, detail="Course code already exists")
    
    return CourseService.create_course(db, course_in)

@router.get("/{code}", response_model=CourseRead)
def get_course(
    code: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    course = CourseService.get_course_by_code(db, code)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/{code}/enrollments", response_model=list[EnrollmentRead])
def get_course_enrollments(
    code: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    course = CourseService.get_course_by_code(db, code)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course.enrollments

@router.get("/", response_model=list[CourseRead])
def list_courses(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    return CourseService.list_courses(db)

@router.delete("/{code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    code: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete courses")

    course = CourseService.get_course_by_code(db, code)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    CourseService.delete_course(db, course)