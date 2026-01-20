import os

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to a pipe-delimited file.

    Args:
        enriched_transactions (list of dicts): Enriched transaction data
        filename (str): Output file path

    File Format:
        TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
        T001|2024-12-01|P101|Laptop|2|45000.0|C001|North|laptops|Apple|4.7|True
    """

    os.makedirs(os.path.dirname(filename), exist_ok=True)


    header = [
        'TransactionID', 'Date', 'ProductID', 'ProductName',
        'Quantity', 'UnitPrice', 'CustomerID', 'Region',
        'API_Category', 'API_Brand', 'API_Rating', 'API_Match'
    ]

    with open(filename, 'w', encoding='utf-8') as f:

        f.write('|'.join(header) + '\n')

      
        for txn in enriched_transactions:
            row = [
                str(txn.get('TransactionID', '')),
                str(txn.get('Date', '')),
                str(txn.get('ProductID', '')),
                str(txn.get('ProductName', '')),
                str(txn.get('Quantity', '')),
                str(txn.get('UnitPrice', '')),
                str(txn.get('CustomerID', '')),
                str(txn.get('Region', '')),
                str(txn.get('API_Category') or ''),  
                str(txn.get('API_Brand') or ''),     
                str(txn.get('API_Rating') or ''),   
                str(txn.get('API_Match', False))
            ]
            f.write('|'.join(row) + '\n')

    print(f"Enriched data saved to '{filename}'")
