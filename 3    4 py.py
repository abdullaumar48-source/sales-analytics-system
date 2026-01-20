import requests

def search_products(query, limit=30):
    """
    Search products by keyword

    Args:
        query (str): Search term
        limit (int): Number of products to return (default 30)

    Returns:
        list of dicts: List of products matching the search
    """
    url = "https://dummyjson.com/products/search"
    params = {"q": query, "limit": limit}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data["products"]

    except requests.exceptions.RequestException as e:
        print(f"Error searching products: {e}")
        return []
{
  "id": 1,
  "title": "iPhone 9",
  "description": "An apple mobile...",
  "price": 549,
  "category": "smartphones",
  "brand": "Apple",
  "rating": 4.69,
  "stock": 94
}
