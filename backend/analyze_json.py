import json

with open('../fayjewelry_products.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('Main categories:', list(data.keys()))
print()

# Check first category structure
first_cat = list(data.keys())[0]
print(f'First category: {first_cat}')
print('Subcategories:', list(data[first_cat].keys()))
print()

# Check first subcategory
first_subcat = list(data[first_cat].keys())[0]
print(f'First subcategory: {first_subcat}')
print('Number of products:', len(data[first_cat][first_subcat]))
if data[first_cat][first_subcat]:
    print('Sample product keys:', list(data[first_cat][first_subcat][0].keys()))
    print('Sample product:', data[first_cat][first_subcat][0])
else:
    print('No products in this subcategory')
