from pydantic import BaseModel
from typing import Optional


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None

    class Config:
        from_attributes = True   # SQLAlchemy ORM support