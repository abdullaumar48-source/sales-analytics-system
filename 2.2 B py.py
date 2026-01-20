2.2 
def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue

    Args:
        transactions (list of dict): Each dict must have keys
            'date', 'quantity', 'price'

    Returns:
        tuple: (date, total_revenue, transaction_count)
    """

    daily_summary = {}

    for txn in transactions:
        date = txn['date']
        quantity = int(txn['quantity'])
        price = float(txn['price'])

        revenue = quantity * price

        if date not in daily_summary:
            daily_summary[date] = {
                'revenue': 0.0,
                'transaction_count': 0
            }

        daily_summary[date]['revenue'] += revenue
        daily_summary[date]['transaction_count'] += 1

    peak_date, peak_data = max(
        daily_summary.items(),
        key=lambda x: x[1]['revenue']
    )

    return (
        peak_date,
        peak_data['revenue'],
        peak_data['transaction_count']
    )
