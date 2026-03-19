from sqlalchemy.orm import Session
from app.models.user_model import User, UserDetails

def check_user(db: Session, user_id: int, email: str):
    return db.query(User).filter(
        User.id == user_id,
        User.email == email
    ).first()



def check_user_from_userdetailstable(db: Session,  email: str):
    return db.query(UserDetails).filter(
        UserDetails.email == email
    ).first()






def get_user_by_email(db: Session, email: str):
    return db.query(UserDetails).filter(UserDetails.email == email).first()


def create_user(db: Session, user_data: dict):
    user = UserDetails(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user