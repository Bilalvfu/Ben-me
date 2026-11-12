from typing import List
from app.crud import product as crud_product
from app.core.database import get_db
from app.models import User
from app.schemas.product import ProductCreate, ProductResponse
from app.security import get_admin_user
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[ProductResponse])
def read_products(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), db: Session = Depends(get_db)):
  products = crud_product.get_products(db, skip=skip, limit=limit)
  return products


@router.get("/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
  db_product = crud_product.get_product(db, product_id=product_id)
  if db_product is None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
    )
  return db_product


@router.post(
    "/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
  try:
    return crud_product.create_product(db=db, product=product)
  except ValueError as exc:
    db.rollback()
    raise HTTPException(status_code=404, detail=str(exc))
  except IntegrityError:
    db.rollback()
    raise HTTPException(status_code=400, detail="Product data violates a database constraint")


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_admin_user)):
  try:
    updated = crud_product.update_product(db, product_id, product)
  except ValueError as exc:
    db.rollback()
    raise HTTPException(status_code=404, detail=str(exc))
  except IntegrityError:
    db.rollback()
    raise HTTPException(status_code=400, detail="Product data violates a database constraint")
  if updated is None:
    raise HTTPException(status_code=404, detail="Product not found")
  return updated


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_admin_user)):
  try:
    if not crud_product.delete_product(db, product_id):
      raise HTTPException(status_code=404, detail="Product not found")
  except IntegrityError:
    db.rollback()
    raise HTTPException(status_code=409, detail="Product is referenced by an order")
