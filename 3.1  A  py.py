import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API.

    Returns:
        list of product dictionaries
        Format:
        [
            {
                'id': 1,
                'title': 'iPhone 9',
                'category': 'smartphones',
                'brand': 'Apple',
                'price': 549,
                'rating': 4.69
            },
            ...
        ]
    """
    url = "https://dummyjson.com/products"
    params = {"limit": 100} 
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  
        data = response.json()

        products = [
            {
                "id": p.get("id"),
                "title": p.get("title"),
                "category": p.get("category"),
                "brand": p.get("brand"),
                "price": p.get("price"),
                "rating": p.get("rating")
            }
            for p in data.get("products", [])
        ]

        print(f"Success: Fetched {len(products)} products")
        return products

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch products: {e}")
        return []
