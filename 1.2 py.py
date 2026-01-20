1.2 
def parse_transactions(raw_lines):
    """
    Parses raw sales transaction lines into a clean list of dictionaries.

    Returns:
        list: List of dictionaries with cleaned and typed values
    """
    parsed_data = []

    for line in raw_lines:
        fields = line.split('|')

        if len(fields) != 8:
            continue

        (
            transaction_id,
            date,
            product_id,
            product_name,
            quantity,
            unit_price,
            customer_id,
            region
        ) = fields
        product_name = product_name.replace(',', '')

        try:
            quantity = int(quantity.replace(',', '').strip())
            unit_price = float(unit_price.replace(',', '').strip())

        except ValueError:
           
            continue

        transaction = {
            'TransactionID': transaction_id.strip(),
            'Date': date.strip(),
            'ProductID': product_id.strip(),
            'ProductName': product_name.strip(),
            'Quantity': quantity,
            'UnitPrice': unit_price,
            'CustomerID': customer_id.strip(),
            'Region': region.strip()
        }

        parsed_data.append(transaction)

    return parsed_data

