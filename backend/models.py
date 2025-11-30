from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string"}


class Product(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    url: str
    title: str
    description: str
    details: Optional[Dict[str, Any]] = None
    images: List[str]
    category: str
    subcategory: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

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
