from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. SQLite veritabanı dosyasının adresi
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

# 2. Veritabanı motorunu (engine) kuruyoruz
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Veritabanı oturumlarını (session) yönetecek fabrikayı kuruyoruz
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Tablolarımızın türeyeceği temel sınıfı (Base) oluşturuyoruz
Base = declarative_base()
