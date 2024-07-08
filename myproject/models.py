from flask import Flask;
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import UniqueConstraint
from sqlalchemy import String, Text
from sqlalchemy import ForeignKey
import logging

from sqlalchemy import String, Integer,Date, create_engine, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column, sessionmaker, relationship

class Base(DeclarativeBase):
  def __repr__(self):
    return f"{self.__class__.__name__}(id={self.id})"
  

db = SQLAlchemy(model_class=Base)


class Category(db.Model):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)

    products: Mapped[list['Product']] = relationship('Product', backref='category', lazy=True)

class ProductImage(db.Model):
    __tablename__ = 'product_image'

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(200), nullable=False)

    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    
class Product(db.Model):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=False)
    image: Mapped['ProductImage'] = relationship('ProductImage', uselist=False, backref='product')

def init_db(db_uri='postgresql://anu:1234@localhost:5432/flaskdb'):
    logger = logging.getLogger("FlaskApp")
    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)
    logger.info("Created database")


def get_session(db_uri):
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
