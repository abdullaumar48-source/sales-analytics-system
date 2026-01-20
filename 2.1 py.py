2.1
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Args:
        transactions (list of dict): Each dict must have keys
            'quantity' and 'price'

    Returns:
        float: Total revenue
    """

    total_revenue = 0.0

    for txn in transactions:
        quantity = float(txn['quantity'])
        price = float(txn['price'])
        total_revenue += quantity * price

    return total_revenue
