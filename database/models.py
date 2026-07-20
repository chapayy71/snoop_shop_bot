from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime

class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    telegram_id: Mapped[int]

    age_verified: Mapped[bool] = mapped_column(
        default=False
    )


class Category(Base):

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]

    products = relationship(
        "Product",
        back_populates="category"
    )


class Product(Base):

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]

    description: Mapped[str]

    price: Mapped[int]

    stock: Mapped[int]

    image: Mapped[str | None]

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id")
    )

    category = relationship(
        "Category",
        back_populates="products"
    )

class CartItem(Base):

    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
    ForeignKey("users.id")
    )

    product_id: Mapped[int] = mapped_column(
    ForeignKey("products.id")
    )

    quantity: Mapped[int] = mapped_column(
        default=1
    )

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int]

    customer_name: Mapped[str]

    telegram_username: Mapped[str | None]

    phone: Mapped[str]

    address: Mapped[str]

    total_price: Mapped[float]

    status: Mapped[str] = mapped_column(default="Новый")

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id")
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )

    quantity: Mapped[int]

    price: Mapped[float]

    order = relationship(
        "Order",
        back_populates="items"
    )