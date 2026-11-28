from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Yonetmen(Base):
    __tablename__ = "yonetmenler"

    id = Column(Integer, primary_key=True, index=True)
    ad_soyad = Column(String(120), nullable=False, unique=True, index=True)
    ulke = Column(String(80), nullable=True)

    filmler = relationship("Film", back_populates="yonetmen", cascade="all, delete-orphan")


class Film(Base):
    __tablename__ = "filmler"

    id = Column(Integer, primary_key=True, index=True)
    baslik = Column(String(200), nullable=False, index=True)
    yayin_yili = Column(Integer, nullable=False, index=True)
    tur = Column(String(60), nullable=False, index=True)
    sure_dakika = Column(Integer, nullable=False)
    puan = Column(Float, nullable=True)
    ozet = Column(Text, nullable=True)

    yonetmen_id = Column(Integer, ForeignKey("yonetmenler.id", ondelete="CASCADE"), nullable=False)
    yonetmen = relationship("Yonetmen", back_populates="filmler")
