PRODUCT_PLACE_MAP = {
    "printer": ["office", "electronics_store", "school"],
    "scanner": ["office", "business_center"],
    "computer": ["electronics_store", "school", "office"],
    "router": ["electronics_store", "office"]
}

def get_place_types_for_product(product_name: str):
    product_name = product_name.lower()
    return PRODUCT_PLACE_MAP.get(product_name, ["store"])
