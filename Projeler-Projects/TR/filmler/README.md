# Filmler API
a
Kullanıcıların kendi film koleksiyonlarını yönetebileceği, JWT tabanlı kimlik doğrulama içeren bir FastAPI uygulaması.

Her kullanıcı sadece kendi eklediği filmleri görebilir, güncelleyebilir ve silebilir. Filmler tür (genre) ve izlenme durumuna (watched) göre filtrelenebilir.

## Özellikler

- Kullanıcı kaydı ve girişi (JWT Bearer Token)
- Film ekleme, listeleme, detay görüntüleme, güncelleme ve silme
- Tür (genre) ve izlenme durumu (watched) ile filtreleme
- Kullanıcı bazlı veri izolasyonu (her kullanıcı sadece kendi filmlerini görür)
- SQLite veritabanı
- Otomatik testler (pytest)

## Teknolojiler

- **FastAPI** – Modern, hızlı web framework
- **SQLAlchemy** – ORM
- **Pydantic** – Veri doğrulama
- **Passlib** + **pbkdf2_sha256** – Şifre hashleme
- **python-jose** – JWT token işlemleri
- **SQLite** – Veritabanı
- **pytest** + **TestClient** – Testler
