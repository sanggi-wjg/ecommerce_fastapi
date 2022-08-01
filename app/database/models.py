from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class UserEntity(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement="auto", index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    username = Column(String(20), nullable=False)
    password = Column(String(250), nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    profile_image = Column(String(200), nullable=False, default="user_profile_default.png")

    datetime_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    datetime_updated = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)


class UserAddressEntity(Base):
    __tablename__ = 'user_address'

    id = Column(Integer, primary_key=True, autoincrement="auto", index=True)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("UserEntity", backref='user_address')

    address_id = Column(Integer, ForeignKey('address.id'), nullable=False)
    address = relationship("AddressEntity", backref='user_address')


class AddressEntity(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, autoincrement="auto", index=True)
    zipcode = Column(String(10), nullable=True)
    address_primary = Column(String(200), nullable=False)
    address_detail = Column(String(200), nullable=False)

# class BusinessEntity(Base):
#     __tablename__ = 'business'
#
#     id = Column(Integer, primary_key=True, autoincrement="auto", index=True)
#     business_name = Column(String(100), unique=True, nullable=False, index=True)
#     business_desc = Column(String(200), nullable=False, index=True)
#     logo = Column(String(200), nullable=False, default="business_default.png")
#
#     datetime_created = Column(DateTime(timezone=True), default=datetime.utcnow)
#     datetime_updated = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
#     # 역방향 relation
#     product = relationship("ProductEntity", back_populates="business_id")
#
#
# class ProductEntity(Base):
#     __tablename__ = 'product'
#
#     id = Column(Integer, primary_key=True, autoincrement="auto", index=True)
#     product_name = Column(String(100), nullable=True, index=True)
#     original_price = Column(DECIMAL(10, 2), nullable=False)
#     new_price = Column(DECIMAL(10, 2), nullable=False)
#     percentage_discount = Column(Integer, nullable=False, default=0)
#     product_image = Column(String(200), nullable=False, default="product_default.png")
#
#     datetime_created = Column(DateTime(timezone=True), default=datetime.utcnow)
#     datetime_updated = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
#     # 정방향 relation
#     business_id = Column(Integer, ForeignKey('business.id'), nullable=False)
#     category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
#     # 역방향 relation
#     options = relationship("ProductOptionEntity", back_populates="product_id")
#
#
# class CategoryEntity(Base):
#     __tablename__ = 'category'
#
#     id = Column(Integer, primary_key=True, autoincrement="auto", index=True)
#     category_name = Column(String(100), nullable=True, index=True)
#     category_desc = Column(String(100), nullable=True)
#     # 역방향 relation
#     product_option = relationship("ProductEntity", back_populates="category_id")
#
#
# class ProductOptionEntity(Base):
#     __tablename__ = 'product_option'
#
#     id = Column(Integer, primary_key=True, autoincrement="auto", index=True)
#     # 정방향 relation
#     product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
#     option_id = Column(Integer, ForeignKey('option.id'), nullable=False)
#
#
# class OptionEntity(Base):
#     __tablename__ = 'option'
#
#     id = Column(Integer, primary_key=True, autoincrement="auto", index=True)
#     category_name = Column(String(100), nullable=True, index=True)
#     category_desc = Column(String(100), nullable=True)
#     # 역방향 relation
#     product_option = relationship("ProductOptionEntity", back_populates="option_id")
