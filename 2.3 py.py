2.3
def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales

    Args:
        transactions (list of dict): Each dict must have keys
            'product', 'quantity', 'price'
        threshold (int): Quantity threshold

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

    low_products = [
        (product,
         data['total_quantity'],
         data['total_revenue'])
        for product, data in product_data.items()
        if data['total_quantity'] < threshold
    ]
    low_products.sort(key=lambda x: x[1])

    return low_products
