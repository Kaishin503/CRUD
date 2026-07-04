from fastapi import FastAPI,Depends
from SCHEMAS import ProductCreate,ProductUpdate,ProductStock,UserInfo,Category,Subcategory
from CRUDFUNCTIONS import create_category,create_subcategory,create_product,list_products,search_product,delete_product,update_product,stock_in,stock_out,stock_log,show_stock_log,product_to_csv,log_to_csv,list_categories_and_subcategories,delete_category,delete_subcategory
from AUTH import create_account,login,get_current_user

app = FastAPI()


@app.post("/create-accounts")
def create_accounts(user: UserInfo):
    try:
        message = create_account(user.Username,user.Password)
        return message
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}
    
@app.post("/login")
def log_in(user: UserInfo):
    try:
        message = login(user.Username,user.Password)
        return message
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}

@app.post("/categories")
def categories(info: Category,current_user = Depends(get_current_user)):
    try:
        message = create_category(info.CategoryName)
        return message
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}

@app.post("/subcategories")
def categories(info: Subcategory,current_user = Depends(get_current_user)):
    try:
        message = create_subcategory(info.SubcategoryName,info.CategoryName)
        return message
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}

@app.get("/categories-and-subcategories")
def categories_and_subcategories(current_user = Depends(get_current_user)):
    try:
        message = list_categories_and_subcategories()
        return message
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}

@app.delete("/categories/{id}")
def delete_categories(id: int,current_user = Depends(get_current_user)):
    try:
        message = delete_category(id)
        return message
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}

@app.delete("/subcategories/{id}")
def delete_subcategories(id: int,current_user = Depends(get_current_user)):
    try:
        message = delete_subcategory(id)
        return message
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}
    
@app.post("/products")
def product_creation(product: ProductCreate,current_user = Depends(get_current_user)):
    try:
        message = create_product(product.ProductName,product.ProductCategory,product.ProductSubcategory,product.ProductPrice,product.ProductStock)
        return message
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}
    
@app.get("/products")
def product_list(current_user = Depends(get_current_user)):
    try:
        products = list_products()
        return {"PRODUCTS":products}
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}

@app.get("/products/{id}")
def product_search(id: int,current_user = Depends(get_current_user)):
    try:
        product = search_product(id=id)
        return product
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}

@app.delete("/products/{id}")
def product_delete(id: int,current_user = Depends(get_current_user)):
    try: 
        delete = delete_product(id)
        return delete
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}

@app.put("/products/{id}")
def product_update(id: int,product: ProductUpdate,current_user = Depends(get_current_user)):
    try:
        update = update_product(id,name=product.ProductName,category=product.ProductCategory,subcategory=product.ProductSubcategory,price=product.ProductPrice)
        return update
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}

@app.post("/products/stock-in/{id}")
def stockin(id,amount: ProductStock,current_user = Depends(get_current_user)):
    try:
        message = stock_in(id,amount.Amount)
        stock_log(id,amount.Amount,"STOCK-IN")
        return message
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}

@app.post("/products/stock-out/{id}")
def stockin(id,amount: ProductStock,current_user = Depends(get_current_user)):
    try:
        message = stock_out(id,amount.Amount)
        stock_log(id,amount.Amount,"STOCK-OUT")
        return message
    except ValueError as err:
        return {"ERROR_MESSAGE":str(err)}

@app.get("/stock-log")
def stocklog(current_user = Depends(get_current_user)):
    log = show_stock_log()
    return log


@app.get("/export-products")
def export(current_user = Depends(get_current_user)):
    return product_to_csv()

@app.get("/export-log")
def export(current_user = Depends(get_current_user)):
    return log_to_csv()

