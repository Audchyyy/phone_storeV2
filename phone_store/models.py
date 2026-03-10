from phone_store.extensions import db, login_manager
from flask_login import UserMixin
from sqlalchemy import Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
    id:       Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email:    Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    fullname: Mapped[str] = mapped_column(String(100), nullable=True)
    avatar:   Mapped[str] = mapped_column(String(50), default='default.png')

    products:   Mapped[List['Product']]  = relationship(back_populates='user')
    cart_items: Mapped[List['CartItem']] = relationship(back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User: {self.username}>'

class Product(db.Model):
    id:          Mapped[int]   = mapped_column(Integer, primary_key=True)
    name:        Mapped[str]   = mapped_column(String(100), nullable=False)
    subtitle:    Mapped[str]   = mapped_column(String(255), nullable=True)
    description: Mapped[str]   = mapped_column(Text, nullable=True)
    price:       Mapped[float] = mapped_column(Float, nullable=False)
    category:    Mapped[str]   = mapped_column(String(50), nullable=True)
    image_url:   Mapped[str]   = mapped_column(String(500), nullable=True)
    model_url:   Mapped[str]   = mapped_column(String(500), nullable=True)
    badge:       Mapped[str]   = mapped_column(String(50), nullable=True)
    user_id:     Mapped[int]   = mapped_column(Integer, ForeignKey('user.id'), nullable=True)

    user: Mapped['User'] = relationship(back_populates='products')

    def __repr__(self):
        return f'<Product: {self.name}>'

class CartItem(db.Model):
    id:         Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id:    Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id'), nullable=False)
    quantity:   Mapped[int] = mapped_column(Integer, default=1)
    added_at:   Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user:    Mapped['User']    = relationship(back_populates='cart_items')
    product: Mapped['Product'] = relationship()

    def subtotal(self):
        return self.product.price * self.quantity

    def __repr__(self):
        return f'<CartItem: {self.product_id} x{self.quantity}>'
