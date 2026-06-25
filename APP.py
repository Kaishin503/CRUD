from fastapi import FastAPI
from SCHEMAS import ProductCreate
from CRUDFUNCTIONS import create_product,list_products

app = FastAPI()



@app.post("/products")
def product_creation(product: ProductCreate):
    try:
        message = create_product(product.ProductName,product.ProductCategory,product.ProductSubcategory,product.ProductPrice,product.ProductStock)
        return message
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}
@app.get("/products")
def product_list():
    try:
        products = list_products()
        return {"PRODUCTS":products}
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}


