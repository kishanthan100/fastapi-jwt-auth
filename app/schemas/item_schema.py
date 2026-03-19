from pydantic import BaseModel
from typing import Optional


class ItemsResponse(BaseModel):
    id: int
    item_name: str
    category: str
    territory: str

    class Config:
        from_attributes = True   # SQLAlchemy ORM support