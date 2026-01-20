2.1 
def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Args:
        transactions (list of dict): Each dict must have keys
            'customer_id', 'product', 'quantity', 'price'

    Returns:
        dict: Customer-wise purchase statistics sorted by total_spent (descending)
    """

    customer_data = {}

    for txn in transactions:
        customer = txn['customer_id']
        product = txn['product']
        quantity = int(txn['quantity'])
        price = float(txn['price'])

        amount = quantity * price

        if customer not in customer_data:
            customer_data[customer] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set()
            }
        customer_data[customer]['total_spent'] += amount
        customer_data[customer]['purchase_count'] += 1
        customer_data[customer]['products_bought'].add(product)


    for customer in customer_data:
        customer_data[customer]['avg_order_value'] = round(
            customer_data[customer]['total_spent'] /
            customer_data[customer]['purchase_count'], 2
        )
        customer_data[customer]['products_bought'] = list(
            customer_data[customer]['products_bought']
        )
    sorted_customers = dict(
        sorted(
            customer_data.items(),
            key=lambda x: x[1]['total_spent'],
            reverse=True
        )
    )

    return sorted_customers
