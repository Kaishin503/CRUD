from pydantic import BaseModel

class ProductCreate(BaseModel):
    ProductName: str
    ProductCategory: str
    ProductSubcategory: str
    ProductPrice: float
    ProductStock: int