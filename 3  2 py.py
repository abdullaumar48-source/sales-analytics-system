3 
import requests

def get_product_by_id(product_id):
    url = f"https://dummyjson.com/products/{product_id}"
    response = requests.get(url)
    response.raise_for_status()  
    return response.json()
