from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.api.depends import get_db, get_current_active_user, RoleChecker
from app.schemas.enrollment import EnrollmentCreate, EnrollmentRead
from app.schemas.user import UserRole
from app.models.course import Course
from app.models.enrollment import Enrollment

router = APIRouter()

@router.post("/{course_id}")
def enroll(
    # course_id: uuid.UUID,
    course_title: str,
    course_code: str,
    # enrollment_in: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(RoleChecker([UserRole.STUDENT]))
):

    # course = db.query(Course).filter(Course.id == course_id, Course.is_active == True).first()
    course =db.query(Course).filter(Course.title == course_title, Course.code == course_code, Course.is_active == True).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found or not active")

    # count = db.query(Enrollment).filter(Enrollment.course_id == course_id).count()
    count = db.query(Enrollment).join(Course).filter(Course.title == course_title, Course.code == course_code).count()
    if count >= course.capacity:
        raise HTTPException(status_code=400, detail="Course is full")

    # new_enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
    new_enrollment = Enrollment(user_id=current_user.id, course_title=course_title, course_code=course_code)
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return {"status": "enrolled"}

@router.get("/{course_id}", response_model=list[EnrollmentRead])
def get_enrollments(
    course_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user = Depends(RoleChecker([UserRole.ADMIN]))
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course.enrollments

@router.get("/", dependencies=[Depends(RoleChecker([UserRole.ADMIN]))])
def get_all_enrollments(db: Session = Depends(get_db)):
    return db.query(Enrollment).all()