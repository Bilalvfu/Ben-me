# Görev Yöneticisi API

FastAPI kullanılarak geliştirilmiş, JWT tabanlı kimlik doğrulama içeren basit bir görev yönetim API'si.

## Özellikler

- Kullanıcı kaydı ve girişi (JWT)
- Şifrelerin güvenli şekilde hash'lenmesi
- Korumalı CRUD işlemleri (Task oluşturma, listeleme, güncelleme, silme)
- Pydantic ile veri doğrulama
- SQLite veritabanı
- Temel unit testler

## Teknolojiler

- **Backend:** FastAPI
- **ORM:** SQLAlchemy
- **Authentication:** JWT (python-jose)
- **Password Hashing:** Passlib (pbkdf2_sha256)
- **Veritabanı:** SQLite
- **Test:** Pytest + TestClient
