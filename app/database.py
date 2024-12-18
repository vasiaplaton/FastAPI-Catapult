from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.config import file_settings

SQLALCHEMY_DATABASE_URL = file_settings.database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
