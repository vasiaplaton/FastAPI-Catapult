from app.database import SessionLocal


def get_db():
    """Get db object"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()
