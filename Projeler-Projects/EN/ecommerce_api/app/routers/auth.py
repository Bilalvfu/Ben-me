from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.crud import user as crud_user
from app.core.database import get_db
from app.models import User
from app.schemas.user import UserCreate, UserResponse
from app.security import (
    create_access_token,
    get_current_user,
    verify_password,
)
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
  db_user = crud_user.get_user_by_email(db, email=user.email)
  if db_user:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="There is already a user registered with this email address.",
    )
  return crud_user.create_user(db=db, user=user)


@router.post("/login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
  user = crud_user.get_user_by_email(db, email=form_data.username)

  if not user or not verify_password(form_data.password, user.hashed_password):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Geçersiz e-posta veya şifre",
        headers={"WWW-Authenticate": "Bearer"},
    )

  access_token = create_access_token(data={"sub": user.email})
  return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
  return current_user
