from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv, find_dotenv
from models import Product, CategoryResponse, SubcategoryResponse
import product_services
# Try to load env file from both .env and env (for compatibility)
if os.path.exists('env'):
    load_dotenv('env')
else:
    load_dotenv(find_dotenv())


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

@app.get("/")
async def root():
    return {"message": "Fay Jewelry API"}

@app.get("/products")
async def get_all_products(page: int = 1, size: int = 10):
    """Get all products with pagination"""
    try:
        product_pagination = await product_services.get_all_products(page, size)
        return product_pagination
    except Exception as e:
        print(f"Error fetching all products: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/products/{product_id}")
async def get_product_by_id(product_id: str):
    """Get a product by its ID"""
    try:
        product = await product_services.get_product_by_id(product_id)
        if product:
            return product
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        print(f"Error fetching product by ID: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")