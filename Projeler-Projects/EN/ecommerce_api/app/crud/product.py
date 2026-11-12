from app.models import Category, Product
from app.schemas.product import ProductCreate
from sqlalchemy.orm import Session


def get_products(db: Session, skip: int = 0, limit: int = 100):
  return db.query(Product).offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int):
  return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, product: ProductCreate):
  if not db.query(Category).filter(Category.id == product.category_id).first():
    raise ValueError("Category not found")
  db_product = Product(**product.model_dump())
  db.add(db_product)
  db.commit()
  db.refresh(db_product)
  return db_product


def update_product(db: Session, product_id: int, product: ProductCreate):
  db_product = get_product(db, product_id)
  if db_product is None:
    return None
  if not db.query(Category).filter(Category.id == product.category_id).first():
    raise ValueError("Category not found")
  for key, value in product.model_dump().items():
    setattr(db_product, key, value)
  db.commit()
  db.refresh(db_product)
  return db_product


def delete_product(db: Session, product_id: int):
  db_product = get_product(db, product_id)
  if db_product is None:
    return False
  db.delete(db_product)
  db.commit()
  return True
