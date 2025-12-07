from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token, LoginRequest
from app.core.security import verify_password, get_password_hash, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account is inactive")
    
    user.last_login = datetime.utcnow()
    db.commit()
    
    access_token = create_access_token(subject=user.id)
    return Token(access_token=access_token, token_type="bearer")

@router.post("/login/json", response_model=Token)
async def login_json(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account is inactive")
    
    user.last_login = datetime.utcnow()
    db.commit()
    
    access_token = create_access_token(subject=user.id)
    return Token(access_token=access_token, token_type="bearer")
