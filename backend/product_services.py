from models import Product, ProductDto, ProductPagination
from typing import List
import os 
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

MONGODB_URL = "mongodb://admin:secret123@localhost:27017"
client = AsyncIOMotorClient(MONGODB_URL)
db = client.e_shop


async def get_all_products(page: int = 1, size: int = 10) -> ProductPagination:
    """Fetch all products with pagination"""
    skip = (page - 1) * size
    total = await db.products.count_documents({})
    total_pages = (total + size - 1) // size  # Ceiling division

    products_cursor = db.products.find().skip(skip).limit(size)
    products = []
    async for product in products_cursor:
        product_dto = ProductDto(
            id=str(product["_id"]),
            url=product.get("url"),
            title=product.get("title"),
            description=product.get("description"),
            image=product.get("images", [None])[0],
            category=product.get("category"),
            subcategory=product.get("subcategory"),
        )
        products.append(product_dto)

    return ProductPagination(
        page=page,
        size=size,
        total=total,
        total_pages=total_pages,
        data=products
    )

async def get_product_by_id(product_id: str) -> Product:
    """Fetch a single product by its ID"""
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    if product:
        return Product(
            id=str(product["_id"]),
            url=product.get("url"),
            title=product.get("title"),
            description=product.get("description"),
            details=product.get("details"),
            images=product.get("images"),
            category=product.get("category"),
            subcategory=product.get("subcategory"),
        )
    return None

