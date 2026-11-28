from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Yonetmen
from app.schemas import YonetmenGuncelle, YonetmenOlustur, YonetmenYanit

router = APIRouter(
    prefix="/yonetmenler",
    tags=["Yönetmenler"],
)


@router.post("/", response_model=YonetmenYanit, status_code=status.HTTP_201_CREATED)
def yonetmen_olustur(yonetmen: YonetmenOlustur, db: Session = Depends(get_db)):
    yeni_yonetmen = Yonetmen(**yonetmen.model_dump())
    db.add(yeni_yonetmen)
    try:
        db.commit()
        db.refresh(yeni_yonetmen)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu isimde bir yönetmen zaten kayıtlı.",
        )
    return yeni_yonetmen


@router.get("/", response_model=list[YonetmenYanit])
def yonetmenleri_listele(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(Yonetmen).offset(skip).limit(limit).all()


@router.get("/{yonetmen_id}", response_model=YonetmenYanit)
def yonetmen_getir(yonetmen_id: int, db: Session = Depends(get_db)):
    yonetmen = db.query(Yonetmen).filter(Yonetmen.id == yonetmen_id).first()
    if not yonetmen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Yönetmen bulunamadı.",
        )
    return yonetmen


@router.patch("/{yonetmen_id}", response_model=YonetmenYanit)
def yonetmen_guncelle(
    yonetmen_id: int,
    yonetmen_veri: YonetmenGuncelle,
    db: Session = Depends(get_db),
):
    yonetmen = db.query(Yonetmen).filter(Yonetmen.id == yonetmen_id).first()
    if not yonetmen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Yönetmen bulunamadı.",
        )

    guncel_alanlar = yonetmen_veri.model_dump(exclude_unset=True)
    for alan, deger in guncel_alanlar.items():
        setattr(yonetmen, alan, deger)

    try:
        db.commit()
        db.refresh(yonetmen)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu isimde başka bir yönetmen kayıtlı.",
        )
    return yonetmen


@router.delete("/{yonetmen_id}", status_code=status.HTTP_204_NO_CONTENT)
def yonetmen_sil(yonetmen_id: int, db: Session = Depends(get_db)):
    yonetmen = db.query(Yonetmen).filter(Yonetmen.id == yonetmen_id).first()
    if not yonetmen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Yönetmen bulunamadı.",
        )
    db.delete(yonetmen)
    db.commit()
    return None