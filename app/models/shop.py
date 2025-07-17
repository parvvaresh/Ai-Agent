from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey,
    Text, Enum
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    """Customer model"""
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20))
    address = Column(String(500))
    city = Column(String(100))
    country = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship: one customer has many orders
    orders = relationship("Order", back_populates="customer")


class Product(Base):
    """Product model"""
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    brand = Column(String(100))
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship: one product has many order items
    order_items = relationship("OrderItem", back_populates="product")


class Order(Base):
    """Order model"""
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    shipping_address = Column(String(500))
    status = Column(Enum('Pending', 'Shipped', 'Delivered', 'Cancelled', name='order_status'), default='Pending')
    payment_method = Column(String(100))
    total_amount = Column(Float, nullable=False)

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    """Order item model"""
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    discount_percent = Column(Integer, default=0)

    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

    @property
    def total_price(self):
        """Calculate total price with discount"""
        return self.price * self.quantity * (1 - self.discount_percent / 100)
