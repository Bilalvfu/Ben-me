from typing import List
from app.crud import order as crud_order
from app.core.database import get_db
from app.models import User
from app.schemas.order import OrderCreate, OrderResponse
from app.security import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post(
    "/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED
)
def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),  
):
  try:
    order = crud_order.create_order(
        db=db, order_in=order_in, user_id=current_user.id
    )
    return order
  except ValueError as e:
    db.rollback()
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
  return crud_order.get_user_orders(db=db, user_id=current_user.id)


@router.get("/{order_id}", response_model=OrderResponse)
def get_my_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  order = crud_order.get_user_order(db, order_id, current_user.id)
  if order is None:
    raise HTTPException(status_code=404, detail="Order not found")
  return order
