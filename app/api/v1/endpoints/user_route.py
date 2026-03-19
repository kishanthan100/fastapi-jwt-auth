from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.user_service import fetch_users
from app.schemas.user_schema import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):

    return fetch_users(db)