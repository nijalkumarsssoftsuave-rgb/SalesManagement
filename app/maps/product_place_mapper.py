CATEGORY_TO_PLACE_TYPES = {
    "electronics": ["electronics_store"],
    "printer": ["electronics_store", "office"],
    "mobile": ["electronics_store", "mobile_phone_store"],
    "network": ["electronics_store", "office"],
    "computer": ["electronics_store", "school", "office"]
}

def get_place_types_for_categories(categories: list[str]):
    place_types = set()

    for category in categories:
        if category in CATEGORY_TO_PLACE_TYPES:
            place_types.update(CATEGORY_TO_PLACE_TYPES[category])
        else:
            place_types.add("store")  # safe fallback

    return list(place_types)
