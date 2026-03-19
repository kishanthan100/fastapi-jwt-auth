from sqlalchemy import Column, Integer, String
from app.core.database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)



class UserDetails(Base):
    __tablename__ = "users_details"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    nic = Column(String)
    address = Column(String)
    phone = Column(String)