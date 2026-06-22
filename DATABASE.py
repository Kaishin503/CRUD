from sqlalchemy import create_engine,String,ForeignKey,Column,Integer,DateTime,text,Float,CheckConstraint
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(f"mysql+pymysql://{os.getenv("DB_USER")}:{os.getenv("DB_PWRD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}",echo=True)
class Base(DeclarativeBase):
    pass

class Product_Category(Base):
    __tablename__ = "PRODUCT_CATEGORY"
    CategoryID = Column("CATEGORY_ID",Integer,primary_key=True,autoincrement=True)
    CategoryName = Column("CATEGORY_NAME",String(100),unique=True,nullable=False)
    CreationDate = Column("CREATION_DATE",DateTime,server_default=text("CURRENT_TIMESTAMP"))

class Product_Subcategory(Base):
    __tablename__ = "PRODUCT_SUBCATEGORY"
    SubcategoryID = Column("SUBCATEGORY_ID",Integer,primary_key=True,autoincrement=True)
    SubcategoryName = Column("SUBCATEGORY_NAME",String(100),unique=True,nullable=False)
    CategoryID = Column("CATEGORY_ID",Integer,ForeignKey("PRODUCT_CATEGORY.CATEGORY_ID",ondelete="CASCADE"),nullable=False)
    CreationDate = Column("CREATION_DATE",DateTime,server_default=text("CURRENT_TIMESTAMP"))

class Products(Base):
    __tablename__ = "PRODUCTS"
    ProductID = Column("PRODUCT_ID",Integer,primary_key=True,autoincrement=True)
    ProductName = Column("PRODUCT_NAME",String(100),unique=True,nullable=False)
    ProductCategory = Column("PRODUCT_CATEGORY_ID",Integer,ForeignKey("PRODUCT_CATEGORY.CATEGORY_ID",ondelete="CASCADE"),nullable=False)
    ProductSubcategory = Column("PRODUCT_SUBCATEGORY_ID",Integer,ForeignKey("PRODUCT_SUBCATEGORY.SUBCATEGORY_ID",ondelete="CASCADE"),nullable=False)
    Price = Column("PRODUCT_PRICE",Float,CheckConstraint("PRODUCT_PRICE >= 0",name="PRODUCT_PRICE_0"),nullable=False)
    Stock = Column("PRODUCT_STOCK",Integer,CheckConstraint("PRODUCT_STOCK >= 0",name="PRODUCT_STOCK_0"),nullable=False)
    CreationDate = Column("CREATION_DATE",DateTime,server_default=text("CURRENT_TIMESTAMP"))
Base.metadata.create_all(bind=engine)