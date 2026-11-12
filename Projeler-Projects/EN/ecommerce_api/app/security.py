import base64
import hashlib
import os
from datetime import datetime, timedelta, timezone

import bcrypt
from app.crud import user as crud_user
from app.core.database import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = os.getenv("SECRET_KEY", "")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable must be set")
if len(SECRET_KEY.encode("utf-8")) < 32:
    raise RuntimeError("SECRET_KEY must contain at least 32 bytes")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

_HASH_PREFIX = "app-bcrypt-sha256$"


def _bcrypt_input(password: str) -> bytes:
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.b64encode(digest)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        if hashed_password.startswith(_HASH_PREFIX):
            encoded_hash = hashed_password[len(_HASH_PREFIX):].encode("ascii")
            return bcrypt.checkpw(_bcrypt_input(plain_password), encoded_hash)

        # Keep existing bcrypt hashes usable during the transition.
        return bcrypt.checkpw(
            plain_password.encode("utf-8")[:72], hashed_password.encode("ascii")
        )
    except (ValueError, TypeError, UnicodeEncodeError):
        return False


def get_password_hash(password: str) -> str:
    hashed = bcrypt.hashpw(_bcrypt_input(password), bcrypt.gensalt())
    return _HASH_PREFIX + hashed.decode("ascii")


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud_user.get_user_by_email(db, email=email)
    if user is None or not user.is_active:
        raise credentials_exception
    return user


def get_admin_user(current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required",
        )
    return current_user
