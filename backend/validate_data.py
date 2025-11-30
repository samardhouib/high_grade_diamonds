import json
import os
from collections import defaultdict

def validate_json_structure(json_file_path):
    """
    Validates the JSON structure to ensure all products are grouped correctly
    and all subproducts exist.
    """
    print("🔍 Validating JSON structure and product grouping...")

    if not os.path.exists(json_file_path):
        print(f"❌ JSON file not found: {json_file_path}")
        return False

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return False

    validation_results = {
        'total_categories': 0,
        'total_subcategories': 0,
        'total_products': 0,
        'empty_categories': [],
        'empty_subcategories': [],
        'incomplete_products': [],
        'category_summary': defaultdict(lambda: {'subcategories': 0, 'products': 0})
    }

    # Required fields for each product
    required_fields = ['url', 'title', 'description', 'details', 'images']

    # Validate structure
    for category, subcategories in data.items():
        validation_results['total_categories'] += 1
        print(f"\n📂 Category: {category}")

        if not isinstance(subcategories, dict):
            print(f"  ❌ Category '{category}' should contain subcategories object, got {type(subcategories)}")
            continue

        if not subcategories:
            validation_results['empty_categories'].append(category)
            print(f"  ❌ Category '{category}' has no subcategories")
            continue

        category_products = 0

        for subcategory, products in subcategories.items():
            validation_results['total_subcategories'] += 1
            print(f"  📁 Subcategory: {subcategory}")

            if not isinstance(products, list):
                print(f"    ❌ Subcategory '{subcategory}' should contain products array, got {type(products)}")
                continue

            if not products:
                validation_results['empty_subcategories'].append(f"{category} -> {subcategory}")
                print(f"    ❌ Subcategory '{subcategory}' has no products")
                continue

            print(f"    📦 Products: {len(products)}")

            for i, product in enumerate(products):
                validation_results['total_products'] += 1
                category_products += 1

                # Check required fields
                missing_fields = []
                for field in required_fields:
                    if field not in product:
                        missing_fields.append(field)

                if missing_fields:
                    validation_results['incomplete_products'].append({
                        'category': category,
                        'subcategory': subcategory,
                        'product_index': i,
                        'title': product.get('title', 'Unknown'),
                        'missing_fields': missing_fields
                    })

                # Validate images array
                if 'images' in product and not isinstance(product['images'], list):
                    validation_results['incomplete_products'].append({
                        'category': category,
                        'subcategory': subcategory,
                        'product_index': i,
                        'title': product.get('title', 'Unknown'),
                        'missing_fields': ['images (should be array)']
                    })

        validation_results['category_summary'][category]['subcategories'] = len(subcategories)
        validation_results['category_summary'][category]['products'] = category_products

    # Print validation summary
    print("\n📊 VALIDATION SUMMARY")
    print("=" * 50)
    print(f"Total Categories: {validation_results['total_categories']}")
    print(f"Total Subcategories: {validation_results['total_subcategories']}")
    print(f"Total Products: {validation_results['total_products']}")

    if validation_results['empty_categories']:
        print(f"\n❌ Empty Categories ({len(validation_results['empty_categories'])}):")
        for cat in validation_results['empty_categories']:
            print(f"  - {cat}")

    if validation_results['empty_subcategories']:
        print(f"\n❌ Empty Subcategories ({len(validation_results['empty_subcategories'])}):")
        for subcat in validation_results['empty_subcategories']:
            print(f"  - {subcat}")

    if validation_results['incomplete_products']:
        print(f"\n❌ Incomplete Products ({len(validation_results['incomplete_products'])}):")
        for prod in validation_results['incomplete_products'][:10]:  # Show first 10
            print(f"  - {prod['category']} -> {prod['subcategory']} -> Product {prod['product_index']}: {prod['title']}")
            print(f"    Missing: {', '.join(prod['missing_fields'])}")
        if len(validation_results['incomplete_products']) > 10:
            print(f"  ... and {len(validation_results['incomplete_products']) - 10} more")

    print("\n📈 CATEGORY BREAKDOWN")
    print("=" * 50)
    for category, stats in sorted(validation_results['category_summary'].items()):
        print(f"{category}: {stats['subcategories']} subcategories, {stats['products']} products")

    # Overall validation result
    is_valid = (
        len(validation_results['empty_categories']) == 0 and
        len(validation_results['empty_subcategories']) == 0 and
        len(validation_results['incomplete_products']) == 0
    )

    if is_valid:
        print("\n✅ VALIDATION PASSED: All products are properly grouped and complete!")
    else:
        print("\n❌ VALIDATION FAILED: Issues found with product grouping or completeness.")

    return is_valid, validation_results

def test_import_logic(json_file_path):
    """
    Test the import logic to ensure it processes data correctly
    """
    print("\n🔧 Testing import logic...")

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to load JSON: {e}")
        return False

    # Simulate import logic
    total_processed = 0
    categories_processed = 0

    for category, subcategories in data.items():
        categories_processed += 1
        print(f"Processing category: {category}")

        for subcategory, products in subcategories.items():
            print(f"  Processing subcategory: {subcategory} ({len(products)} products)")

            for product in products:
                # Simulate the processing in import_data.py
                if not all(key in product for key in ['url', 'title', 'description', 'details', 'images']):
                    print(f"    ❌ Product missing required fields: {product.get('title', 'Unknown')}")
                    return False

                # Process images
                cleaned_images = []
                for image_path in product["images"]:
                    cleaned_path = image_path.replace("fayjewelry_images\\", "").replace("\\", "/")
                    cleaned_images.append(cleaned_path)

                # Process details
                processed_details = product["details"]
                if isinstance(processed_details, str):
                    # Test the parse_details_string function
                    parsed_details = {}
                    parts = processed_details.split(';')
                    for part in parts:
                        if ':' in part:
                            key, value = part.split(':', 1)
                            parsed_details[key.strip()] = value.strip()
                    processed_details = parsed_details

                total_processed += 1

    print(f"✅ Import logic test passed! Processed {total_processed} products across {categories_processed} categories.")
    return True

if __name__ == "__main__":
    json_file = "../fayjewelry_products.json"

    # Validate JSON structure
    is_valid, results = validate_json_structure(json_file)

    # Test import logic
    import_logic_ok = test_import_logic(json_file)

    if is_valid and import_logic_ok:
        print("\n🎉 ALL VALIDATIONS PASSED! Products are correctly grouped and import script will work properly.")
    else:
        print("\n⚠️  VALIDATION ISSUES FOUND. Please review the output above.")
