from pydantic import BaseModel, ConfigDict
from typing import Optional

# --- Kullanıcı Şemaları ---
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)

# --- Token Şemaları ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Film Şemaları ---
class MovieCreate(BaseModel):
    title: str
    director: str
    release_year: int
    genre: str
    watched: Optional[bool] = False

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    director: Optional[str] = None
    release_year: Optional[int] = None
    genre: Optional[str] = None
    watched: Optional[bool] = None

class MovieResponse(BaseModel):
    id: int
    title: str
    director: str
    release_year: int
    genre: str
    watched: bool
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
