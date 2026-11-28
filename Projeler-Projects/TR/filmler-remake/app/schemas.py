from typing import Optional
from pydantic import BaseModel, Field


# --- Yönetmen Şemaları ---
class YonetmenBase(BaseModel):
    ad_soyad: str = Field(..., min_length=2, max_length=120, examples=["Christopher Nolan"])
    ulke: Optional[str] = Field(default=None, max_length=80, examples=["Birleşik Krallık"])


class YonetmenOlustur(YonetmenBase):
    pass


class YonetmenGuncelle(BaseModel):
    ad_soyad: Optional[str] = Field(default=None, min_length=2, max_length=120)
    ulke: Optional[str] = Field(default=None, max_length=80)


class YonetmenYanit(YonetmenBase):
    id: int

    model_config = {"from_attributes": True}


# --- Film Şemaları ---
class FilmBase(BaseModel):
    baslik: str = Field(..., min_length=1, max_length=200, examples=["Inception"])
    yayin_yili: int = Field(..., ge=1888, le=2100, examples=[2010])
    tur: str = Field(..., min_length=2, max_length=60, examples=["Bilim Kurgu"])
    sure_dakika: int = Field(..., gt=0, le=1000, examples=[148])
    puan: Optional[float] = Field(default=None, ge=0.0, le=10.0, examples=[8.8])
    ozet: Optional[str] = Field(default=None, examples=["Rüyalar içinde rüya kurgulanan bir bilim kurgu filmi."])
    yonetmen_id: int = Field(..., gt=0, examples=[1])


class FilmOlustur(FilmBase):
    pass


class FilmGuncelle(BaseModel):
    baslik: Optional[str] = Field(default=None, min_length=1, max_length=200)
    yayin_yili: Optional[int] = Field(default=None, ge=1888, le=2100)
    tur: Optional[str] = Field(default=None, min_length=2, max_length=60)
    sure_dakika: Optional[int] = Field(default=None, gt=0, le=1000)
    puan: Optional[float] = Field(default=None, ge=0.0, le=10.0)
    ozet: Optional[str] = None
    yonetmen_id: Optional[int] = Field(default=None, gt=0)


class FilmYanit(FilmBase):
    id: int
    yonetmen: Optional[YonetmenYanit] = None

    model_config = {"from_attributes": True}
