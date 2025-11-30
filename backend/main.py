from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv, find_dotenv
from models import Product, CategoryResponse, SubcategoryResponse

# Try to load env file from both .env and env (for compatibility)
if os.path.exists('env'):
    load_dotenv('env')
else:
    load_dotenv(find_dotenv())

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://admin:secret123@mongodb:27017/e_shop?authSource=admin")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.e_shop

app = FastAPI(title="Fay Jewelry API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:3004",
        "http://frontend:3000",  # Docker service name
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (images)
app.mount("/images", StaticFiles(directory="../fayjewelry_images"), name="images")

@app.get("/")
async def root():
    return {"message": "Fay Jewelry API"}

@app.get("/categories", response_model=CategoryResponse)
async def get_categories():
    """Get all product categories"""
    categories = await db.products.distinct("category")
    return CategoryResponse(categories=categories)

@app.get("/categories/{category}/products")
async def get_products_by_category(category: str):
    """Get all products in a specific category"""
    try:
        products = await db.products.find({"category": category}).to_list(None)

        # Convert ObjectId to string for JSON serialization
        for product in products:
            product["_id"] = str(product["_id"])

        return {"products": products}
    except Exception as e:
        print(f"Error fetching products for category {category}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/products/{product_id}")
async def get_product(product_id: str):
    """Get a specific product by ID"""
    try:
        product = await db.products.find_one({"_id": ObjectId(product_id)})
        if product:
            product["_id"] = str(product["_id"])
            return product
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        print(f"Error fetching product {product_id}: {e}")
        raise HTTPException(status_code=400, detail="Invalid product ID or database error")

@app.get("/categories/{category}/subcategories", response_model=SubcategoryResponse)
async def get_subcategories(category: str):
    """Get subcategories for a specific category"""
    subcategories = await db.products.distinct("subcategory", {"category": category})
    return SubcategoryResponse(subcategories=subcategories)

@app.get("/categories/{category}/{subcategory}/products")
async def get_products_by_subcategory(category: str, subcategory: str):
    """Get products by category and subcategory"""
    products = await db.products.find({"category": category, "subcategory": subcategory}).to_list(None)

    # Convert ObjectId to string for JSON serialization
    for product in products:
        product["_id"] = str(product["_id"])

    return {"products": products}

@app.get("/home/products-by-subcategory")
async def get_products_by_subcategory_home():
    """Get all products grouped by subcategory for homepage"""
    try:
        # Get all products
        all_products = await db.products.find({}).to_list(None)
        
        # Convert ObjectId to string and group by subcategory
        grouped = {}
        for product in all_products:
            product["_id"] = str(product["_id"])
            subcategory = product.get("subcategory", "Other")
            category = product.get("category", "Other")
            
            if subcategory not in grouped:
                grouped[subcategory] = {
                    "subcategory": subcategory,
                    "category": category,
                    "products": []
                }
            grouped[subcategory]["products"].append(product)
        
        # Convert to list and limit products per subcategory to 8 for homepage
        result = []
        for subcategory, data in grouped.items():
            result.append({
                "subcategory": data["subcategory"],
                "category": data["category"],
                "products": data["products"][:8]  # Limit to 8 products per subcategory
            })
        
        return {"subcategories": result}
    except Exception as e:
        print(f"Error fetching products by subcategory: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
