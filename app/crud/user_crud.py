from sqlalchemy.orm import Session
from app.models.user_model import User

def get_users(db: Session):
    return db.query(User).all()