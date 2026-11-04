from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest

from database import Base
from main import app, get_db

# SQLite bellek içi veritabanının tüm bağlantılar tarafından paylaşılmasını sağlıyoruz
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def setup_database():
    # Her testten önce tabloları oluştur
    Base.metadata.create_all(bind=engine)
    yield
    # Test bittikten sonra tabloları temizle
    Base.metadata.drop_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_register_user():
    response = client.post("/register", json={"username": "testuser", "password": "securepassword"})
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data

def test_login_and_create_task():
    # Önce kullanıcıyı kaydedelim
    client.post("/register", json={"username": "testuser", "password": "securepassword"})

    # Giriş yapıp token alalım
    response = client.post("/token", data={"username": "testuser", "password": "securepassword"})
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    token = token_data["access_token"]

    # Korumalı endpoint'e istek atalım
    headers = {"Authorization": f"Bearer {token}"}
    task_response = client.post("/tasks", json={"title": "Test Görevi", "description": "Test açıklaması"}, headers=headers)
    
    assert task_response.status_code == 201
    task_data = task_response.json()
    assert task_data["title"] == "Test Görevi"
    assert task_data["completed"] == False
