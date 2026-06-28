from fastapi import FastAPI
from SCHEMAS import ProductCreate,ProductUpdate, ProductStock
from CRUDFUNCTIONS import create_product,list_products,search_product,delete_product,update_product,stock_in,stock_out,stock_log,show_stock_log,product_to_csv,log_to_csv

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

@app.get("/products/{id}")
def product_search(id: int):
    try:
        product = search_product(id=id)
        return product
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}

@app.delete("/products/{id}")
def product_delete(id: int):
    try: 
        delete = delete_product(id)
        return delete
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}

@app.put("/products/{id}")
def product_update(id: int,product: ProductUpdate):
    try:
        update = update_product(id,name=product.ProductName,category=product.ProductCategory,subcategory=product.ProductSubcategory,price=product.ProductPrice)
        return update
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}

@app.post("/products/stock-in/{id}")
def stockin(id,amount: ProductStock):
    try:
        message = stock_in(id,amount.Amount)
        stock_log(id,amount.Amount,"STOCK-IN")
        return message
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}

@app.post("/products/stock-out/{id}")
def stockin(id,amount: ProductStock):
    try:
        message = stock_out(id,amount.Amount)
        stock_log(id,amount.Amount,"STOCK-OUT")
        return message
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}


@app.get("/stock-log")
def stocklog():
    log = show_stock_log()
    return log

@app.get("/export-products")
def export():
    return product_to_csv()

@app.get("/export-log")
def export():
    return log_to_csv()
    