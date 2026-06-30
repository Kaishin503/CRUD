from DATABASE import engine,Products,Product_Category,Product_Subcategory,StockLog,User
from sqlalchemy.orm import Session
from datetime import datetime
import pandas as pd
from fastapi.responses import StreamingResponse
import io
import bcrypt
from datetime import datetime,timedelta,timezone
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_account(name,password):
    with Session(engine) as session:
        if len(name) <= 4:
            raise ValueError("NAME MUST BE ABOVE 4 CHARACTERS")
        name_validation = session.query(User).filter(User.Username == name).first()
        if name_validation is not None:
            raise ValueError("NAME ALREADY TAKEN")
        if len(password) <= 8:
            raise ValueError("PASSWORD LENGTH MUST BE ABOVE 8 CHARACTERS")
        hash = bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt())
        hashed_pw = hash.decode("utf-8")
        new_user = User(
            Username = name,
            Password = hashed_pw
        )
        session.add(new_user)
        session.commit()
        session.close()
        return {"MESSAGE":"ACCOUNT CREATED"}

def login(name,password):
    with Session(engine) as session:
        user_search = session.query(User).filter(User.Username == name).first()
        if user_search is None:
            raise ValueError("USER NOT FOUND")
        stored_hash = user_search.Password.encode("utf-8")
        password = password.encode("utf-8")
        if not bcrypt.checkpw(password,stored_hash):
            raise ValueError("INCORRECT PASSWORD")
        payload = {
                "sub": str(user_search.UserID),
                "exp":datetime.now(timezone.utc) + timedelta(minutes=30)
            }
        token = jwt.encode(payload,os.getenv("SECRET_KEY"),algorithm=os.getenv("ALGORITHM"))
        return {"TOKEN":token}
        
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
        token,
        os.getenv("SECRET_KEY"),
        algorithms=[os.getenv("ALGORITHM")]
    )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="USER NOT FOUND"
        )
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="INVALID TOKEN"
        )
    with Session(engine) as session:
        user = session.query(User).filter(User.UserID == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="USER NOT FOUND"
            )
        return user
    

def create_product(name,category,subcategory,price,init_stock):
    with Session(engine) as session:
        name_verification = session.query(Products.ProductName).filter(Products.ProductName == name).first()
        if name_verification is not None:
            raise ValueError("PRODUCT NAME TAKEN")
        
        category_validation = session.query(Product_Category.CategoryID).filter(Product_Category.CategoryName == category).first()
        if category_validation is None:
            raise ValueError("CATEGORY DOES NOT EXIST")
        
        subcategory_verification = session.query(Product_Subcategory.SubcategoryID).filter(Product_Subcategory.SubcategoryName == subcategory).first()
        if subcategory_verification is None:
            raise ValueError("SUBCATEGORY DOES NOT EXIST")
        
        subcategory_validation = session.query(Product_Subcategory).filter(Product_Subcategory.SubcategoryID == subcategory_verification,Product_Subcategory.CategoryID == category_validation)
        if subcategory_validation is None:
            raise("SUBCATEGORY DOES NOT BELONG TO THIS CATEGORY")
        
        if price <= 0:
            raise ValueError("PRICE CANNOT BE LESS THAN/EQUAL TO 0")
        
        if init_stock <= 0:
            raise ValueError("INITIAL STOCK CANNOT BE LOWER THAN/EQUAL TO 0")

        product = Products(
            ProductName = name,
            ProductCategory = category_validation[0],
            ProductSubcategory = subcategory_verification[0],
            Price = price,
            Stock = init_stock
        )
        
        session.add(product)
        session.commit()
        session.close()
        return {"SYSTEM_MESSAGE":"PRODUCT SUCCESSFULLY CREATED"}

def list_products():
    with Session(engine) as session:
        product_list = []
        products = session.query(Products,Product_Category.CategoryName,Product_Subcategory.SubcategoryName).join(Product_Category, Products.ProductCategory == Product_Category.CategoryID).join(Product_Subcategory, Product_Category.CategoryID == Product_Subcategory.CategoryID).all()
        if len(products) == 0:
            raise ValueError("NO PRODUCT FOUND")
        for item in products:
            product_list.append({item[0].ProductID:[item[0].ProductName,item[0].ProductCategory,item[1],item[2],item[0].ProductSubcategory,item[0].Price,item[0].Stock]})
        return product_list

def search_product(id=None):
    if id is not None:
        with Session(engine) as session: 
            product = session.query(Products,Product_Category.CategoryName,Product_Subcategory.SubcategoryName).join(Product_Category, Products.ProductCategory == Product_Category.CategoryID).join(Product_Subcategory, Product_Category.CategoryID == Product_Subcategory.CategoryID).filter(Products.ProductID == id).first()
            if product is None:
                raise ValueError("PRODUCT NOT FOUND")
            else:
                return {product[0].ProductID:[product[0].ProductName,product[0].ProductCategory,product[1],product[2],product[0].ProductSubcategory,product[0].Price,product[0].Stock]}   
    else:
        raise ValueError("ID ARGUMENT NOT GIVEN")
    
def update_product(id,name=None,category=None,subcategory=None,price=None):
    with Session(engine) as session:
        product = session.query(Products).filter(Products.ProductID == id).first()
        if product is None:
            raise ValueError("PRODUCT NOT FOUND")
        
        if name is not None:
            product_validation = session.query(Products).filter(Products.ProductName == name).first()
            if product_validation is not None:
                raise ValueError("PRODUCT NAME ALREADY EXISTS")
            product.ProductName = name

        if category is not None:
            category_validation = session.query(Product_Category.CategoryID).filter(Product_Category.CategoryName == category).first()
            if category_validation is None:
                raise ValueError("CATEGORY DOES NOT EXIST")
            product.ProductCategory = category_validation
        
        if subcategory is not None:
            subcategory_verification = session.query(Product_Subcategory.SubcategoryID).filter(Product_Subcategory.SubcategoryName == subcategory).first()
            if subcategory_verification is None:
                raise ValueError("SUBCATEGORY DOES NOT EXIST")
            subcategory_validation = session.query(Product_Subcategory).filter(Product_Subcategory.SubcategoryID == subcategory_verification,Product_Subcategory.CategoryID == category_validation)
            if subcategory_validation is None:
                raise ValueError("SUBCATEGORY DOES NOT BELONG TO THIS CATEGORY")
            product.ProductSubcategory = subcategory

        if price is not None:
            if price <= 0:
                raise ValueError("PRICE CANNOT BE LOWER THAN/EQUAL TO 0:")
            product.Price = price
        
        session.commit()
        session.close()

    return {"MESSAGE":"PRODUCT UPDATED"}
        
def delete_product(id):
    with Session(engine) as session:
        product = session.query(Products).filter(Products.ProductID == id).first()
        if product is None:
            raise ValueError("PRODUCT NOT FOUND")
        else:
            session.delete(product)
            session.commit()
            session.close()
            return {"MESSAGE":"PRODUCT DELETED"}

def stock_in(id,amount):
    with Session(engine) as session:
        product_stock = session.query(Products.Stock).filter(Products.ProductID == id).first()
        if product_stock is None:
            raise ValueError("PRODUCT NOT FOUND")
        product_stock = session.query(Products).filter(Products.ProductID == id).update({Products.Stock:Products.Stock + amount})
        session.commit()
        session.close()
        return {"MESSSAGE":"STOCK-IN DONE"}

def stock_out(id,amount):
    with Session(engine) as session:
        product_stock = session.query(Products.Stock).filter(Products.ProductID == id).first()
        if product_stock is None:
            raise ValueError("PRODUCT NOT FOUND")
        product_stock = session.query(Products).filter(Products.ProductID == id).update({Products.Stock:Products.Stock - amount})
        session.commit()
        session.close()
        return {"MESSSAGE":"STOCK-OUT DONE"}

def stock_log(id,amount,type):
    with Session(engine) as session:
        new_log = StockLog(
            Type = type,
            Amount = amount,
            ProductID = id
        )
        session.add(new_log)
        session.commit()
        session.close()

def show_stock_log():
    with Session(engine) as session:
        list_log = []
        log_list = session.query(StockLog).all()
        for item in log_list:
            date = datetime.strftime(item.Date,"%H:%M:%S, %d/%m/%Y")
            list_log.append({item.LogID:{"TYPE":item.Type,"AMOUNT":item.Amount,"PRODUCT_ID":item.ProductID,"DATE":date}})
        return list_log

def product_to_csv():
    df = pd.read_sql("SELECT * FROM Products",engine)
    output = io.StringIO()
    df.to_csv(output,index=False)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition":"attachment; filename=Products.csv"
        }
    )
def log_to_csv():
    df = pd.read_sql("SELECT * FROM STOCK_LOG",engine)
    output = io.StringIO()
    df.to_csv(output,index=False)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition":"attachment; filename=Stock.csv"
        }
    )