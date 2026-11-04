from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite veritabanı dosya yolu (Films projesi için ayrı bir DB dosyası kullanıyoruz)
SQLALCHEMY_DATABASE_URL = "sqlite:///./films.db"

# SQLite için thread (iş parçacığı) kısıtlamasını kaldıran argüman
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Her istek (request) için veritabanı oturumu açacak sınıf
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modellerimizin miras alacağı temel sınıf (Base)
Base = declarative_base()

# FastAPI bağımlılığı (Dependency Injection) için veritabanı oturumu sağlayan fonksiyon
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
