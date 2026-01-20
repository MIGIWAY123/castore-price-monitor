from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

# Модель товара
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String, unique=True)

# Модель истории цен
class PriceHistory(Base):
    __tablename__ = 'price_history'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.now)

# Создаем файл базы данных
engine = create_engine('sqlite:///prices.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)