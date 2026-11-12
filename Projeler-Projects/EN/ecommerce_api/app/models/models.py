from datetime import datetime
from app.core.database import Base
from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship


class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  email = Column(String, unique=True, index=True, nullable=False)
  hashed_password = Column(String, nullable=False)
  is_active = Column(Boolean, default=True)
  is_admin = Column(Boolean, default=False)
  created_at = Column(DateTime, default=datetime.utcnow)

  
  orders = relationship("Order", back_populates="user")


class Category(Base):
  __tablename__ = "categories"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, unique=True, index=True, nullable=False)
  slug = Column(String, unique=True, index=True, nullable=False)
  description = Column(Text, nullable=True)

  
  products = relationship("Product", back_populates="category")


class Product(Base):
  __tablename__ = "products"
  __table_args__ = (
      CheckConstraint("price >= 0", name="ck_products_price_nonnegative"),
      CheckConstraint("stock >= 0", name="ck_products_stock_nonnegative"),
  )

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True, nullable=False)
  description = Column(Text, nullable=True)
  price = Column(Numeric(10, 2), nullable=False)
  stock = Column(Integer, default=0, nullable=False)
  category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow)

  
  category = relationship("Category", back_populates="products")
  order_items = relationship("OrderItem", back_populates="product")


class Order(Base):
  __tablename__ = "orders"
  __table_args__ = (CheckConstraint("total_price >= 0", name="ck_orders_total_nonnegative"),)

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  total_price = Column(Numeric(12, 2), nullable=False)
  status = Column(
      String, default="pending"
  )  
  created_at = Column(DateTime, default=datetime.utcnow)

  
  user = relationship("User", back_populates="orders")
  items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
  __tablename__ = "order_items"
  __table_args__ = (CheckConstraint("quantity > 0", name="ck_order_items_quantity_positive"),)

  id = Column(Integer, primary_key=True, index=True)
  order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
  product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
  quantity = Column(Integer, nullable=False)
  unit_price = Column(Numeric(10, 2), nullable=False)


  order = relationship("Order", back_populates="items")
  product = relationship("Product", back_populates="order_items")
