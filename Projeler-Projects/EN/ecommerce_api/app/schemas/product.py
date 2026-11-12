from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
  name: str
  description: Optional[str] = None
  price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
  stock: int = Field(ge=0)
  category_id: int = Field(gt=0)


class ProductCreate(ProductBase):
  pass


class ProductResponse(ProductBase):
  id: int

  model_config = ConfigDict(from_attributes=True)
