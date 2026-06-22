from sqlalchemy import create_engine,String,ForeignKey,Column,Integer,DateTime,text
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
