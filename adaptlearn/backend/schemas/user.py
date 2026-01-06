from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserGoogleCreate(UserBase):
    picture: Optional[str] = None
    auth_provider: str = "google"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    picture: Optional[str] = None
    
    class Config:
        from_attributes = True
