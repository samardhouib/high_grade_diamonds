import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_data():
    client = AsyncIOMotorClient('mongodb://admin:secret123@localhost:27017')
    try:
        db = client.e_shop
        # Get one product from Semi Mount Rings category
        product = await db.products.find_one({'category': 'Semi Mount Rings'})
        if product:
            print('Sample product from Semi Mount Rings:')
            print(f'_id: {product.get("_id")}')
            print(f'category: {product.get("category")}')
            print(f'subcategory: {product.get("subcategory")}')
            print(f'details type: {type(product.get("details"))}')
            details = product.get('details', {})
            if isinstance(details, dict):
                print(f'details keys: {list(details.keys())}')
                print(f'details: {details}')
            else:
                print(f'details: {details}')
        else:
            print('No product found in Semi Mount Rings category')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(check_data())
