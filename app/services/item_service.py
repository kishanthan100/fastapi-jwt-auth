from sqlalchemy.orm import Session
from app.crud.item_crud import get_items, get_item_by_id


def fetch_items(db: Session):
    items = get_items(db)
    return items


def get_item_id_details(db: Session, item_id: int):
    return get_item_by_id(db, item_id) 