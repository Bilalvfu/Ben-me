from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import text
from fastapi import FastAPI, Depends, status, HTTPException

import models
import schemas
import database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Kişisel Film Kütüphanesi API",
    description="MySQL ve JSON destekli profesyonel film kütüphanesi portfolyo projesi",
    version="1.0.0"
)

@app.post("/filmler/", response_model=schemas.Film, status_code=status.HTTP_201_CREATED)
def film_olustur(film: schemas.FilmCreate, db: Session = Depends(database.get_db)):
    
    db_film = models.FilmModel(
        isim=film.isim,
        cikis_yili=film.cikis_yili,
        yapimci=film.yapimci,
        detaylar=film.detaylar
    )
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    return db_film

@app.get("/filmler/", response_model=List[schemas.Film])
def film_listele(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    filmler = db.query(models.FilmModel).offset(skip).limit(limit).all()
    return filmler

@app.get("/filmler/filtrele/detay", response_model=List[schemas.Film])
def detaylara_gore_filtrele(anahtar: str, deger: str, db: Session = Depends(database.get_db)):
    """
    JSON detaylar alanı içinde dinamik arama yapar.
    Örnek Kullanım: /filmler/filtrele/detay?anahtar=yonetmen&deger=Christopher Nolan
    """
    
    filmler = db.query(models.FilmModel).filter(
        models.FilmModel.detaylar[anahtar].as_string() == f'"{deger}"'
    ).all()
    
    return filmler

@app.put("/filmler/{film_id}", response_model=schemas.Film)
def film_guncelle(film_id: int, film: schemas.FilmCreate, db: Session = Depends(database.get_db)):
    """
    Belirtilen ID'ye sahip filmin bilgilerini günceller.
    """
    db_film = db.query(models.FilmModel).filter(models.FilmModel.id == film_id).first()
    
    if db_film is None:
        raise HTTPException(status_code=404, detail="Güncellenmek istenen film bulunamadı.")
    
    db_film.isim = film.isim
    db_film.cikis_yili = film.cikis_yili
    db_film.yapimci = film.yapimci
    db_film.detaylar = film.detaylar
    
    db.commit()
    db.refresh(db_film)
    return db_film



@app.delete("/filmler/{film_id}", status_code=status.HTTP_204_NO_CONTENT)
def film_sil(film_id: int, db: Session = Depends(database.get_db)):
    """
    Belirtilen ID'ye sahip filmi veritabanından siler.
    """
    db_film = db.query(models.FilmModel).filter(models.FilmModel.id == film_id).first()
    
    if db_film is None:
        raise HTTPException(status_code=404, detail="Silinmek istenen film bulunamadı.")
    
    db.delete(db_film)
    db.commit()
    return None
