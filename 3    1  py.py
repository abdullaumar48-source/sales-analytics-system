3 

import requests

def get_all_products(limit=30):
    response = requests.get('https://dummyjson.com/products')
    data = response.json()

    return data['products'][:limit]
