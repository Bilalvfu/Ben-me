from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Film, Yonetmen
from app.schemas import FilmGuncelle, FilmOlustur, FilmYanit

router = APIRouter(
    prefix="/filmler",
    tags=["Filmler"],
)


@router.post("/", response_model=FilmYanit, status_code=status.HTTP_201_CREATED)
def film_olustur(film: FilmOlustur, db: Session = Depends(get_db)):
    yonetmen = db.query(Yonetmen).filter(Yonetmen.id == film.yonetmen_id).first()
    if not yonetmen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Belirtilen yönetmen bulunamadı.",
        )

    yeni_film = Film(**film.model_dump())
    db.add(yeni_film)
    db.commit()
    db.refresh(yeni_film)
    return yeni_film


@router.get("/", response_model=list[FilmYanit])
def filmleri_listele(
    arama: Optional[str] = Query(default=None, description="Film başlığında arama yapar"),
    tur: Optional[str] = Query(default=None, description="Türe göre filtreler"),
    yayin_yili: Optional[int] = Query(default=None, description="Yayın yılına göre filtreler"),
    min_puan: Optional[float] = Query(default=None, ge=0.0, le=10.0, description="Minimum puan filtresi"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    sorgu = db.query(Film)

    if arama:
        sorgu = sorgu.filter(Film.baslik.ilike(f"%{arama.strip()}%"))
    if tur:
        sorgu = sorgu.filter(Film.tur.ilike(tur.strip()))
    if yayin_yili is not None:
        sorgu = sorgu.filter(Film.yayin_yili == yayin_yili)
    if min_puan is not None:
        sorgu = sorgu.filter(Film.puan >= min_puan)

    return sorgu.offset(skip).limit(limit).all()


@router.get("/{film_id}", response_model=FilmYanit)
def film_getir(film_id: int, db: Session = Depends(get_db)):
    film = db.query(Film).filter(Film.id == film_id).first()
    if not film:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Film bulunamadı.",
        )
    return film


@router.patch("/{film_id}", response_model=FilmYanit)
def film_guncelle(film_id: int, film_veri: FilmGuncelle, db: Session = Depends(get_db)):
    film = db.query(Film).filter(Film.id == film_id).first()
    if not film:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Film bulunamadı.",
        )

    guncel_alanlar = film_veri.model_dump(exclude_unset=True)

    if "yonetmen_id" in guncel_alanlar:
        yonetmen = db.query(Yonetmen).filter(Yonetmen.id == guncel_alanlar["yonetmen_id"]).first()
        if not yonetmen:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Belirtilen yeni yönetmen bulunamadı.",
            )

    for alan, deger in guncel_alanlar.items():
        setattr(film, alan, deger)

    db.commit()
    db.refresh(film)
    return film


@router.delete("/{film_id}", status_code=status.HTTP_204_NO_CONTENT)
def film_sil(film_id: int, db: Session = Depends(get_db)):
    film = db.query(Film).filter(Film.id == film_id).first()
    if not film:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Film bulunamadı.",
        )
    db.delete(film)
    db.commit()
    return None