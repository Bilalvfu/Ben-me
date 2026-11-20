from fastapi import Depends, FastAPI
from app.routers import comments, posts, tags, users
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.routers import users

app = FastAPI(title="Blog API")

app.include_router(users.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(tags.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Blog API is running"}


@app.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "connected"}
