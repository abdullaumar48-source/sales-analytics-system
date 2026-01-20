3   
import requests

def get_products(limit=30):
    """
    Fetches a specific number of products from DummyJSON.

    Args:
        limit (int): Number of products to fetch

    Returns:
        list of dicts: List of product objects
    """
    url = "https://dummyjson.com/products"
    params = {"limit": limit}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  
        data = response.json()
        return data["products"]

    except requests.exceptions.RequestException as e:
        print(f"Error fetching products: {e}")
        return []
