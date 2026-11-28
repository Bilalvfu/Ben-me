from fastapi import FastAPI

from app.database import Base, engine
from app.routers import filmler, yonetmenler

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Filmler API",
    description="FastAPI, SQLAlchemy ve PostgreSQL ile geliştirilmiş film ve yönetmen yönetim servisi.",
    version="1.0.0",
)

app.include_router(yonetmenler.router)
app.include_router(filmler.router)


@app.get("/", tags=["Genel"])
def ana_sayfa():
    return {
        "mesaj": "Filmler API çalışıyor.",
        "dokumantasyon": "/docs",
    }


@app.get("/health", tags=["Genel"])
def saglik_kontrolu():
    return {"durum": "tamam"}
