from typing import List
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
  product_id: int = Field(gt=0)
  quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
  items: List[OrderItemCreate] = Field(min_length=1)


class OrderItemResponse(BaseModel):
  id: int
  product_id: int
  quantity: int
  unit_price: Decimal

  model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
  id: int
  total_price: Decimal
  status: str
  items: List[OrderItemResponse]

  model_config = ConfigDict(from_attributes=True)
