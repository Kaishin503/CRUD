from DATABASE import engine,Products,Product_Category,Product_Subcategory
from sqlalchemy.orm import Session


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
