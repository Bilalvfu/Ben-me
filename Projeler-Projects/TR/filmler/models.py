from sqlalchemy import Column, Integer, String, JSON
from database import Base 

class FilmModel(Base):
    __tablename__ = "filmler"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    isim = Column(String(255), nullable=False)
    cikis_yili = Column(Integer, nullable=False)
    yapimci = Column(String(255), nullable=False)
    detaylar = Column(JSON, nullable=True)
