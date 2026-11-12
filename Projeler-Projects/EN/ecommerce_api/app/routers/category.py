from app.crud import category as crud_category
from app.core.database import get_db
from app.schemas.category import CategoryCreate, CategoryResponse
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import User
from app.security import get_admin_user

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryResponse])
def read_categories(
    skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), db: Session = Depends(get_db)
):
  return crud_category.get_categories(db, skip=skip, limit=limit)


@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_admin_user)):
  try:
    return crud_category.create_category(db=db, category=category)
  except IntegrityError:
    db.rollback()
    raise HTTPException(status_code=409, detail="Category name or slug already exists")


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_admin_user)):
  try:
    updated = crud_category.update_category(db, category_id, category)
  except IntegrityError:
    db.rollback()
    raise HTTPException(status_code=409, detail="Category name or slug already exists")
  if updated is None:
    raise HTTPException(status_code=404, detail="Category not found")
  return updated


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_admin_user)):
  try:
    if not crud_category.delete_category(db, category_id):
      raise HTTPException(status_code=404, detail="Category not found")
  except IntegrityError:
    db.rollback()
    raise HTTPException(status_code=409, detail="Category still has products")
