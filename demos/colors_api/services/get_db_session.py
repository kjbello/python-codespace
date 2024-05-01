from typing import Generator
from sqlalchemy.orm import Session
from database import SessionLocal


# dependency injected db session
def get_db_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
