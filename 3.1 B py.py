def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info

    Args:
        api_products (list of dicts): Output from fetch_all_products()

    Returns:
        dict: Mapping of product IDs to info
        Format:
        {
            1: {'title': 'iPhone 9', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.69},
            2: {...},
        }
    """
    product_mapping = {}

    for product in api_products:
        product_id = product.get("id")
        if product_id is not None:
            product_mapping[product_id] = {
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"),
                "rating": product.get("rating")
            }

    return product_mapping
