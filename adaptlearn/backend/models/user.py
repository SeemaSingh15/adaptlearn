from sqlalchemy import Column, Integer, String, Boolean
from db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    picture = Column(String, nullable=True)
    auth_provider = Column(String, default="email") # email or google
