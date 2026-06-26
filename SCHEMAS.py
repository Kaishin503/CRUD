from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    ProductName: str
    ProductCategory: str
    ProductSubcategory: str
    ProductPrice: float
    ProductStock: int

class ProductUpdate(BaseModel):
    ProductName: Optional[str] = None
    ProductCategory: Optional[str] = None
    ProductSubcategory: Optional[str] = None
    ProductPrice: Optional[float] = None