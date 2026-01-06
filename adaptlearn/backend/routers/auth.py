from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt
from db.session import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin, UserResponse
from schemas.token import Token
from core.security import verify_password, get_password_hash, create_access_token
from config import settings
from google.oauth2 import id_token
from google.auth.transport import requests

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        auth_provider="email"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token_expires = timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/google", response_model=Token)
def google_login(token: str, db: Session = Depends(get_db)):
    try:
        # Verify Google Token
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)
        email = idinfo['email']
        
        user = db.query(User).filter(User.email == email).first()
        if not user:
            # Create user if not exists
            user = User(
                email=email,
                full_name=idinfo.get('name'),
                picture=idinfo.get('picture'),
                auth_provider="google",
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
        access_token_expires = timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Google Token")
