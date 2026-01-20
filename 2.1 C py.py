2.1 
def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Args:
        transactions (list of dict): Each dict must have keys
            'product', 'quantity', 'price'
        n (int): Number of top products to return

    Returns:
        list of tuples:
        (ProductName, TotalQuantity, TotalRevenue)
    """

    product_data = {}

    for txn in transactions:
        product = txn['product']
        quantity = int(txn['quantity'])
        price = float(txn['price'])

        if product not in product_data:
            product_data[product] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }

        product_data[product]['total_quantity'] += quantity
        product_data[product]['total_revenue'] += quantity * price

    result = [
        (product,
         data['total_quantity'],
         data['total_revenue'])
        for product, data in product_data.items()
    ]
    result.sort(key=lambda x: x[1], reverse=True)

    return result[:n]
