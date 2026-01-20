import os
import sys
import traceback
from datetime import datetime
from collections import defaultdict
import requests


def read_sales_data(filename):
    """Read sales data from a file"""
    try:
        for enc in ['utf-8', 'latin-1', 'cp1252']:
            try:
                with open(filename, 'r', encoding=enc) as f:
                    lines = [line.strip() for line in f if line.strip()]
                    return lines[1:]  
            except Exception:
                continue
        print("Error: Unable to read file with known encodings.")
        return []
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []

def fetch_all_products():
    """Fetch all products from DummyJSON API (limit 100)"""
    try:
        response = requests.get("https://dummyjson.com/products?limit=100")
        response.raise_for_status()
        data = response.json()
        return data.get('products', [])
    except Exception as e:
        print("Error fetching products:", e)
        return []

def create_product_mapping(api_products):
    """Create mapping: product ID → info dict"""
    mapping = {}
    for p in api_products:
        mapping[p['id']] = {
            'title': p['title'],
            'category': p['category'],
            'brand': p['brand'],
            'rating': p['rating']
        }
    return mapping

def enrich_sales_data(transactions, product_mapping):
    """Enrich transactions with API data"""
    enriched = []
    for txn in transactions:
        pid_num = ''.join(filter(str.isdigit, txn['ProductID']))
        pid_num = int(pid_num) if pid_num else None
        api_info = product_mapping.get(pid_num)
        enriched_txn = txn.copy()
        if api_info:
            enriched_txn.update({
                'API_Category': api_info['category'],
                'API_Brand': api_info['brand'],
                'API_Rating': api_info['rating'],
                'API_Match': True
            })
        else:
            enriched_txn.update({
                'API_Category': None,
                'API_Brand': None,
                'API_Rating': None,
                'API_Match': False
            })
        enriched.append(enriched_txn)
    return enriched

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    header = [
        'TransactionID', 'Date', 'ProductID', 'ProductName',
        'Quantity', 'UnitPrice', 'CustomerID', 'Region',
        'API_Category', 'API_Brand', 'API_Rating', 'API_Match'
    ]
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('|'.join(header)+'\n')
        for txn in enriched_transactions:
            row = [
                str(txn.get('TransactionID','')),
                str(txn.get('Date','')),
                str(txn.get('ProductID','')),
                str(txn.get('ProductName','')),
                str(txn.get('Quantity','')),
                str(txn.get('UnitPrice','')),
                str(txn.get('CustomerID','')),
                str(txn.get('Region','')),
                str(txn.get('API_Category') or ''),
                str(txn.get('API_Brand') or ''),
                str(txn.get('API_Rating') or ''),
                str(txn.get('API_Match', False))
            ]
            f.write('|'.join(row)+'\n')
    print(f"✓ Enriched data saved to '{filename}'")



def region_wise_sales(transactions):
    region_data = defaultdict(lambda: {'total_sales':0.0,'transaction_count':0})
    for txn in transactions:
        region = txn.get('Region','Unknown')
        region_data[region]['total_sales'] += txn['Quantity']*txn['UnitPrice']
        region_data[region]['transaction_count'] +=1
    total_sales = sum(r['total_sales'] for r in region_data.values())
    for r in region_data:
        region_data[r]['percentage'] = round(region_data[r]['total_sales']/total_sales*100,2) if total_sales else 0
    return dict(sorted(region_data.items(), key=lambda x: x[1]['total_sales'], reverse=True))

def top_selling_products(transactions, n=5):
    product_data = defaultdict(lambda:{'quantity':0,'revenue':0.0})
    for txn in transactions:
        name = txn['ProductName']
        product_data[name]['quantity'] += txn['Quantity']
        product_data[name]['revenue'] += txn['Quantity']*txn['UnitPrice']
    top = sorted(product_data.items(), key=lambda x: x[1]['quantity'], reverse=True)[:n]
    return [(name, data['quantity'], data['revenue']) for name,data in top]

def customer_analysis(transactions):
    customer_data = defaultdict(lambda:{'total_spent':0.0,'purchase_count':0,'products_bought':set()})
    for txn in transactions:
        cid = txn['CustomerID']
        customer_data[cid]['total_spent'] += txn['Quantity']*txn['UnitPrice']
        customer_data[cid]['purchase_count'] +=1
        customer_data[cid]['products_bought'].add(txn['ProductName'])
 
    for cid in customer_data:
        data = customer_data[cid]
        data['avg_order_value'] = round(data['total_spent']/data['purchase_count'],2) if data['purchase_count'] else 0
        data['products_bought'] = list(data['products_bought'])
    return dict(sorted(customer_data.items(), key=lambda x:x[1]['total_spent'], reverse=True))

def main():
    print("="*40)
    print("SALES ANALYTICS SYSTEM")
    print("="*40)
    try:
      
        raw_lines = read_sales_data('data/sales_data.txt')
        transactions=[]
        for line in raw_lines:
            parts=line.split('|')
            if len(parts)!=8: continue
            transactions.append({
                "TransactionID": parts[0],
                "Date": parts[1],
                "ProductID": parts[2],
                "ProductName": parts[3],
                "Quantity": int(parts[4]),
                "UnitPrice": float(parts[5]),
                "CustomerID": parts[6],
                "Region": parts[7]
            })
        print(f"✓ Parsed {len(transactions)} records")

        api_products = fetch_all_products()
        mapping = create_product_mapping(api_products)
        enriched_txns = enrich_sales_data(transactions, mapping)
        save_enriched_data(enriched_txns)

        print("\nRegion-wise sales:")
        print(region_wise_sales(transactions))
        print("\nTop 5 products:")
        print(top_selling_products(transactions))
        print("\nTop customers:")
        print(customer_analysis(transactions))

    except Exception as e:
        print("Error occurred:", e)
        traceback.print_exc()

if __name__=="__main__":
    main()
