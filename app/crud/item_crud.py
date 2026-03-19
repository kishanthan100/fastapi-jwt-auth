from sqlalchemy.orm import Session
from app.models.item_model import Items

def get_items(db: Session):
    return db.query(Items).all()


def get_item_by_id(db: Session, item_id: int):
    return db.query(Items).filter(Items.id == item_id).first()