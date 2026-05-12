from fastapi import FastAPI
import logging
from app.api.v1 import auth as auth_router
from app.api.v1 import course as course_router
from app.api.v1 import enrollment as enrollment_router
from app.core.config import settings


logging.basicConfig(
    level=logging.DEBUG if settings.ENVIRONMENT == "development" else logging.WARNING, 
    format="%(name)s:%(levelname)s:%(message)s")

app = FastAPI(title="Course Enrollment System API")
app.include_router(auth_router.router, prefix=settings.API_V1_STR + "/auth", tags=["auth"])
app.include_router(course_router.router, prefix=settings.API_V1_STR + "/courses", tags=["courses"])
app.include_router(enrollment_router.router, prefix=settings.API_V1_STR + "/enrollments", tags=["enrollments"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Course Registration System API!"}