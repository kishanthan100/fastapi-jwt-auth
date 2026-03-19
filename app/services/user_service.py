from sqlalchemy.orm import Session
from app.crud.user_crud import get_users

def fetch_users(db: Session):

    users = get_users(db)

    return users