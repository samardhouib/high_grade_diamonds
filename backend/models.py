from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from bson import ObjectId



class Product(BaseModel):
    id: Optional[str] = None
    url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    images: Optional[List[str]] = None
    category: Optional[str] = None
    subcategory: Optional[str]= None

class ProductDto(BaseModel):
    id: Optional[str] = None
    url: Optional[str] = None
    title : Optional[str] = None
    description: Optional[str ]= None
    image: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None

class ProductPagination(BaseModel):
    page: Optional[int] = 0
    size: Optional[int] = 10
    total: Optional[int] = 0 
    total_pages : Optional[int] = 0
    data : Optional[List[ProductDto]] = []

class ProductCreate(BaseModel):
    url: str
    title: str
    description: str
    details: Optional[Dict[str, Any]] = None
    images: List[str]
    category: str
    subcategory: str

class CategoryResponse(BaseModel):
    categories: List[str]

class SubcategoryResponse(BaseModel):
    subcategories: List[str]

class ProductsResponse(BaseModel):
    products: List[Product]
