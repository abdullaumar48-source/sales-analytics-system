1.3
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.

    Returns:
        tuple: (valid_transactions, invalid_count, filter_summary)
    """

    valid_transactions = []
    invalid_count = 0

    required_fields = [
        'TransactionID', 'Date', 'ProductID', 'ProductName',
        'Quantity', 'UnitPrice', 'CustomerID', 'Region'
    ]

    
    
    for txn in transactions:

        if not all(field in txn for field in required_fields):
            invalid_count += 1
            continue

        if (
            not txn['TransactionID'].startswith('T') or
            not txn['ProductID'].startswith('P') or
            not txn['CustomerID'].startswith('C')
        ):
            invalid_count += 1
            continue

        if txn['Quantity'] <= 0 or txn['UnitPrice'] <= 0:
            invalid_count += 1
            continue

        valid_transactions.append(txn)


    summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': 0,
        'filtered_by_amount': 0,
        'final_count': 0
    }


 
    available_regions = sorted(
        set(txn['Region'] for txn in valid_transactions)
    )
    print("Available Regions:", available_regions)


    amounts = [
        txn['Quantity'] * txn['UnitPrice']
        for txn in valid_transactions
    ]

    if amounts:
        print(
            f"Transaction Amount Range: "
            f"Min = {min(amounts)}, Max = {max(amounts)}"
        )

    if region:
        before_count = len(valid_transactions)
        valid_transactions = [
            txn for txn in valid_transactions
            if txn['Region'] == region
        ]
        summary['filtered_by_region'] = before_count - len(valid_transactions)
        print(f"After region filter ({region}): {len(valid_transactions)} records")


    if min_amount is not None or max_amount is not None:
        before_count = len(valid_transactions)

        filtered = []
        for txn in valid_transactions:
            amount = txn['Quantity'] * txn['UnitPrice']

            if min_amount is not None and amount < min_amount:
                continue
            if max_amount is not None and amount > max_amount:
                continue

            filtered.append(txn)

        valid_transactions = filtered
        summary['filtered_by_amount'] = before_count - len(valid_transactions)
        print(f"After amount filter: {len(valid_transactions)} records")

    summary['final_count'] = len(valid_transactions)

    return valid_transactions, invalid_count, summary

