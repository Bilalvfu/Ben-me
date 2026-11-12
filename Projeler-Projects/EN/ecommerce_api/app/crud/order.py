from decimal import Decimal
from app.models import Order, OrderItem, Product
from app.schemas.order import OrderCreate
from sqlalchemy.orm import Session


def create_order(db: Session, order_in: OrderCreate, user_id: int):
  quantities: dict[int, int] = {}
  for item in order_in.items:
    quantities[item.product_id] = quantities.get(item.product_id, 0) + item.quantity
  if not quantities:
    raise ValueError("Order must contain at least one item")

  try:
    # The request-scoped session transaction includes stock, order and items.
    products = {}
    for product_id in sorted(quantities):
      product = db.query(Product).filter(Product.id == product_id).with_for_update().first()
      if product is None:
        raise ValueError(f"Product not found: ID {product_id}")
      quantity = quantities[product_id]
      if product.stock < quantity:
        raise ValueError(f"Insufficient stock for {product.name}")
      products[product_id] = product

    total_price = sum((products[pid].price * qty for pid, qty in quantities.items()), Decimal("0.00"))
    db_order = Order(user_id=user_id, total_price=total_price, status="pending")
    db.add(db_order)
    db.flush()
    for product_id, quantity in quantities.items():
      product = products[product_id]
      product.stock -= quantity
      db.add(OrderItem(order_id=db_order.id, product_id=product_id, quantity=quantity, unit_price=product.price))
    db.commit()
    db.refresh(db_order)
    return db_order
  except Exception:
    db.rollback()
    raise


def get_user_orders(db: Session, user_id: int):
  return db.query(Order).filter(Order.user_id == user_id).all()


def get_user_order(db: Session, order_id: int, user_id: int):
  return db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
