import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv, find_dotenv

def parse_details_string(details_string: str) -> dict:
    parsed_details = {}
    if not details_string or not isinstance(details_string, str):
        return parsed_details

    # Split by semicolon to get individual key-value parts
    parts = details_string.split(';')
    for part in parts:
        if ':' in part:
            key, value = part.split(':', 1)  # Split only on the first colon
            parsed_details[key.strip()] = value.strip()
    return parsed_details

# Try to load env file from both .env and env (for compatibility)
if os.path.exists('env'):
    load_dotenv('env')
else:
    load_dotenv(find_dotenv())

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://admin:secret123@localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.e_shop

async def import_data():
    # Load JSON data
    with open('../fayjewelry_products.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Clear existing data
    await db.products.drop()
    print("Cleared existing products collection")

    # Import data
    total_products = 0
    for category, subcategories in data.items():
        print(f"Importing category: {category}")
        for subcategory, products in subcategories.items():
            print(f"  Importing subcategory: {subcategory} ({len(products)} products)")

            # Prepare products for insertion
            products_to_insert = []
            for product in products:
                cleaned_images = []
                for image_path in product["images"]:
                    # Remove 'fayjewelry_images\' prefix and replace backslashes with forward slashes
                    cleaned_path = image_path.replace("fayjewelry_images\\", "").replace("\\", "/")
                    cleaned_images.append(cleaned_path)

                # Process product details
                processed_details = product["details"]
                if isinstance(processed_details, str):
                    processed_details = parse_details_string(processed_details)

                product_doc = {
                    "url": product["url"],
                    "title": product["title"],
                    "description": product["description"],
                    "details": processed_details,
                    "images": cleaned_images,
                    "category": category,
                    "subcategory": subcategory
                }
                products_to_insert.append(product_doc)

            # Insert products in batch
            if products_to_insert:
                result = await db.products.insert_many(products_to_insert)
                total_products += len(result.inserted_ids)
                print(f"    Inserted {len(result.inserted_ids)} products")

    print(f"\nTotal products imported: {total_products}")

    # Create indexes for better performance
    await db.products.create_index("category")
    await db.products.create_index("subcategory")
    await db.products.create_index([("category", 1), ("subcategory", 1)])
    print("Created database indexes")

    # Close connection
    client.close()
    print("Import completed successfully!")

if __name__ == "__main__":
    asyncio.run(import_data())
