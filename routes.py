from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, Token
from auth import authenticate_user, create_access_token, decode_access_token, oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter()


@auth_router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = User(username=user.username)
    new_user.set_password(user.password)
    db.add(new_user)
    db.commit()

    access_token = create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/verify")
def verify(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    return {"username": payload.get("sub")}
