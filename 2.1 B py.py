2.1 
def region_wise_sales(transactions):
    """
    Analyzes sales by region

    Args:
        transactions (list of dict): Each dict must have keys:
            'region' and 'amount'

    Returns:
        dict: Region-wise sales statistics sorted by total_sales (descending)
    """

    region_data = {}
    grand_total = 0.0

   
    for txn in transactions:
        region = txn['region']
        amount = float(txn['amount'])

        if region not in region_data:
            region_data[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }

        region_data[region]['total_sales'] += amount
        region_data[region]['transaction_count'] += 1
        grand_total += amount

   
    for region in region_data:
        region_data[region]['percentage'] = round(
            (region_data[region]['total_sales'] / grand_total) * 100, 2
        )

   
    sorted_data = dict(
        sorted(
            region_data.items(),
            key=lambda x: x[1]['total_sales'],
            reverse=True
        )
    )

    return sorted_data
