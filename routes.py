import logging

from fastapi import FastAPI, Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from passlib.context import CryptContext

from auth import get_password_hash, authenticate_user, create_access_token, decode_access_token, oauth2_scheme
from database import engine, get_db
from models import Base, User
from schemas import Token, UserCreate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_router = APIRouter()


@auth_router.post("/auth/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = User(username=user.username, hashed_password=get_password_hash(user.password))
    db.add(new_user)
    db.commit()

    access_token = create_access_token(data={"sub": new_user.username, "id": new_user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username, "id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


class Token(BaseModel):
    access_token: str


@auth_router.post("/auth/verify")
def verify(body: Token, db: Session = Depends(get_db)):
    payload = decode_access_token(body.access_token)
    username = payload.get("sub")
    user_id = payload.get("id")
    if not username or not user_id:
        raise HTTPException(status_code=400, detail="Token has no id or username")

    user = db.query(User).filter(User.username == username, User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    return {"username": username, "id": user_id}
