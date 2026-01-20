2.2
def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date

    Args:
        transactions (list of dict): Each dict must have keys
            'date', 'customer_id', 'quantity', 'price'

    Returns:
        dict: Date-wise sales statistics sorted chronologically
    """

    daily_data = {}

    for txn in transactions:
        date = txn['date']
        customer = txn['customer_id']
        quantity = int(txn['quantity'])
        price = float(txn['price'])

        revenue = quantity * price

        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'unique_customers': set()
            }

        daily_data[date]['revenue'] += revenue
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['unique_customers'].add(customer)

    sorted_daily = dict(
        sorted(
            daily_data.items(),
            key=lambda x: x[0] 
        )
    )

    for date in sorted_daily:
        sorted_daily[date]['unique_customers'] = len(
            sorted_daily[date]['unique_customers']
        )

    return sorted_daily
