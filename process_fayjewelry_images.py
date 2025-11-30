import json
import codecs
with codecs.open("fayjewelry_products.json", "r", encoding="utf-8") as file:
    data = json.load(file)

new_data = []
for subcategory in data.keys():
    for category in data[subcategory].keys():
        for product in data[subcategory][category]:
            new_product = product.copy()
            new_product["category"] = category
            new_product["subcategory"] = subcategory
            new_data.append(new_product)
with codecs.open("fayjewelry_products_processed.json", "w", encoding="utf-8") as file:
    json.dump(new_data, file, ensure_ascii=False, indent=4)

            