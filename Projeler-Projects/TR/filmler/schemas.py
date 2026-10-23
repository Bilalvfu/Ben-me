from pydantic import BaseModel
from typing import Optional, Dict, Any

class FilmBase(BaseModel):
    isim: str
    cikis_yili: int
    yapimci: str
    detaylar: Optional[Dict[str, Any]] = None  

class FilmCreate(FilmBase):
    pass

class Film(FilmBase):
    id: int

    class Config:
        from_attributes = True
