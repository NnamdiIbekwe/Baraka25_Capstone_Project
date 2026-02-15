from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate


class CourseService:

    @staticmethod
    def create_course(db: Session, course: CourseCreate) -> Course:
        db_course = Course(
            title=course.title,
            code=course.code,
            capacity=course.capacity,
            is_active=course.is_active
        )
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return db_course


    @staticmethod
    def get_course_by_code(db: Session, code: str) -> Course | None:
        return db.query(Course).filter(Course.code == code).first()

    @staticmethod
    def update_course(db: Session, course: Course, course_in: CourseUpdate) -> Course:
        for field, value in course_in.model_dump(exclude_unset=True).items():
            setattr(course, field, value)
        
        db.commit()
        db.refresh(course)
        return course
    
    @staticmethod
    def delete_course(db: Session, course: Course) -> None:
        db.delete(course)
        db.commit()