import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import models
from database import Base, get_db
from main import app

# Bellek içi test veritabanı (StaticPool ile güvenli bağlantı)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Her test öncesi tabloları sıfırdan kur, test bitince uçur
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# --- Test Senaryoları ---

def test_register_user():
    response = client.post(
        "/register",
        json={"username": "sinemasever", "password": "securepassword123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "sinemasever"
    assert "id" in data

def test_login_and_create_movie():
    # 1. Kullanıcı kaydı
    client.post(
        "/register",
        json={"username": "yonetmen", "password": "mypassword"}
    )
    
    # 2. Giriş yap ve Token al
    response = client.post(
        "/token",
        data={"username": "yonetmen", "password": "mypassword"}
    )
    assert response.status_code == 200
    token_data = response.json()
    token = token_data["access_token"]
    
    # 3. Token ile Film Ekle
    headers = {"Authorization": f"Bearer {token}"}
    movie_response = client.post(
        "/movies/",
        json={
            "title": "Interstellar",
            "director": "Christopher Nolan",
            "release_year": 2014,
            "genre": "Sci-Fi",
            "watched": True
        },
        headers=headers
    )
    assert movie_response.status_code == 201
    movie_data = movie_response.json()
    assert movie_data["title"] == "Interstellar"
    assert movie_data["director"] == "Christopher Nolan"
    assert movie_data["watched"] is True

def test_filter_movies():
    # Kullanıcı oluştur ve giriş yap
    client.post("/register", json={"username": "filmest", "password": "password123"})
    token = client.post("/token", data={"username": "filmest", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # İki farklı türde film ekle
    client.post("/movies/", json={"title": "Matrix", "director": "Wachowski", "release_year": 1999, "genre": "Sci-Fi"}, headers=headers)
    client.post("/movies/", json={"title": "The Godfather", "director": "Coppola", "release_year": 1972, "genre": "Crime"}, headers=headers)
    
    # Sadece Sci-Fi filmlerini filtrele
    response = client.get("/movies/?genre=Sci-Fi", headers=headers)
    assert response.status_code == 200
    movies = response.json()
    assert len(movies) == 1
    assert movies[0]["title"] == "Matrix"
