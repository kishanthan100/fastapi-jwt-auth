from pydantic import BaseModel


class LoginRequest(BaseModel):
    id: int
    email: str
    

    class Config:
        from_attributes = True   # SQLAlchemy ORM support