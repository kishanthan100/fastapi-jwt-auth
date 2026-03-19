from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Items(Base):

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String)
    category = Column(String)
    territory = Column(String)
    img_url = Column(String)