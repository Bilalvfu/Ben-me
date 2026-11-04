from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import List, Optional

import models, schemas
from database import engine, get_db

# Veritabanı tablolarını otomatik oluştur
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Films API", version="1.0.0")

# Güvenlik Ayarları (72 bayt limitine takılmayan pbkdf2_sha256 standardı)
SECRET_KEY = "super-secret-key-for-films-project-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Yardımcı Fonksiyonlar ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Mevcut Token'dan Kullanıcıyı Çeken Dependency
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Kimlik bilgileri doğrulanamadı",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


# --- Auth Endpoint'leri ---

@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Bu kullanıcı adı zaten kullanımda")
    
    hashed_password = get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Geçersiz kullanıcı adı veya şifre",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# --- Movie (Film) Endpoint'leri ---

@app.post("/movies/", response_model=schemas.MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(movie: schemas.MovieCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_movie = models.Movie(**movie.model_dump(), owner_id=current_user.id)
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie

@app.get("/movies/", response_model=List[schemas.MovieResponse])
def get_movies(
    genre: Optional[str] = Query(None, description="Türe göre filtrele"),
    watched: Optional[bool] = Query(None, description="İzlenme durumuna göre filtrele"),
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    query = db.query(models.Movie).filter(models.Movie.owner_id == current_user.id)
    
    if genre:
        query = query.filter(models.Movie.genre.ilike(f"%{genre}%"))
    if watched is not None:
        query = query.filter(models.Movie.watched == watched)
        
    return query.all()

@app.get("/movies/{movie_id}", response_model=schemas.MovieResponse)
def get_movie(movie_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id, models.Movie.owner_id == current_user.id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Film bulunamadı")
    return movie

@app.put("/movies/{movie_id}", response_model=schemas.MovieResponse)
def update_movie(movie_id: int, movie_update: schemas.MovieUpdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id, models.Movie.owner_id == current_user.id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Film bulunamadı")
    
    update_data = movie_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(movie, key, value)
        
    db.commit()
    db.refresh(movie)
    return movie

@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id, models.Movie.owner_id == current_user.id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Film bulunamadı")
    
    db.delete(movie)
    db.commit()
    return None
