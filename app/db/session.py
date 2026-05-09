from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.config import settings

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


engine = create_engine(
    settings.DATABASE_URL
)

