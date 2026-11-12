import os

os.environ.setdefault("SECRET_KEY", "test-only-secret-key-that-is-long-enough")
os.environ.setdefault("DATABASE_URL", "sqlite://")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.models import User
from app.security import get_password_hash


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSession()
    db.add(User(email="admin@example.com", hashed_password=get_password_hash("test-password"), is_admin=True))
    db.add(User(email="user@example.com", hashed_password=get_password_hash("test-password")))
    db.commit()
    db.close()

    def override_get_db():
        session = TestingSession()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def token(client, email):
    response = client.post("/auth/login", data={"username": email, "password": "test-password"})
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def admin_headers(client):
    return {"Authorization": f"Bearer {token(client, 'admin@example.com')}"}


@pytest.fixture
def user_headers(client):
    return {"Authorization": f"Bearer {token(client, 'user@example.com')}"}
