"""Use decimal money, category descriptions and data constraints.

Revision ID: 2f8d1c4a6b90
Revises: 777e2ba36d35
"""
from alembic import op
import sqlalchemy as sa

revision = "2f8d1c4a6b90"
down_revision = "777e2ba36d35"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("categories", sa.Column("description", sa.Text(), nullable=True))
    op.alter_column("products", "price", type_=sa.Numeric(10, 2), existing_type=sa.Float(), existing_nullable=False)
    op.alter_column("orders", "total_price", type_=sa.Numeric(12, 2), existing_type=sa.Float(), existing_nullable=False)
    op.alter_column("order_items", "unit_price", type_=sa.Numeric(10, 2), existing_type=sa.Float(), existing_nullable=False)
    op.create_check_constraint("ck_products_price_nonnegative", "products", "price >= 0")
    op.create_check_constraint("ck_products_stock_nonnegative", "products", "stock >= 0")
    op.create_check_constraint("ck_orders_total_nonnegative", "orders", "total_price >= 0")
    op.create_check_constraint("ck_order_items_quantity_positive", "order_items", "quantity > 0")


def downgrade() -> None:
    op.drop_constraint("ck_order_items_quantity_positive", "order_items", type_="check")
    op.drop_constraint("ck_orders_total_nonnegative", "orders", type_="check")
    op.drop_constraint("ck_products_stock_nonnegative", "products", type_="check")
    op.drop_constraint("ck_products_price_nonnegative", "products", type_="check")
    op.alter_column("order_items", "unit_price", type_=sa.Float(), existing_type=sa.Numeric(10, 2), existing_nullable=False)
    op.alter_column("orders", "total_price", type_=sa.Float(), existing_type=sa.Numeric(12, 2), existing_nullable=False)
    op.alter_column("products", "price", type_=sa.Float(), existing_type=sa.Numeric(10, 2), existing_nullable=False)
    op.drop_column("categories", "description")
