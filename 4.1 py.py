import os
from datetime import datetime
from collections import defaultdict

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted sales report and saves to file.

    Args:
        transactions (list of dicts): Original transaction data
        enriched_transactions (list of dicts): Transactions enriched with API info
        output_file (str): File path to save the report
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    report_lines = []
    total_records = len(transactions)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report_lines.append("="*50)
    report_lines.append(" " * 10 + "SALES ANALYTICS REPORT")
    report_lines.append(f"Generated: {now}")
    report_lines.append(f"Records Processed: {total_records}")
    report_lines.append("="*50)
    report_lines.append("")

    total_revenue = sum(float(txn['UnitPrice']) * int(txn['Quantity']) for txn in transactions)
    total_transactions = len(transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = sorted([txn['Date'] for txn in transactions])
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

    report_lines.append("OVERALL SUMMARY")
    report_lines.append("-"*50)
    report_lines.append(f"Total Revenue:        ₹{total_revenue:,.2f}")
    report_lines.append(f"Total Transactions:   {total_transactions}")
    report_lines.append(f"Average Order Value:  ₹{avg_order_value:,.2f}")
    report_lines.append(f"Date Range:           {date_range}")
    report_lines.append("")

    region_data = defaultdict(lambda: {'sales': 0.0, 'count': 0})
    for txn in transactions:
        region = txn.get('Region', 'Unknown')
        region_data[region]['sales'] += float(txn['UnitPrice']) * int(txn['Quantity'])
        region_data[region]['count'] += 1

    total_sales = sum(r['sales'] for r in region_data.values())

    report_lines.append("REGION-WISE PERFORMANCE")
    report_lines.append("-"*50)
    report_lines.append(f"{'Region':<10}{'Sales':>15}{'% of Total':>12}{'Transactions':>15}")
    sorted_regions = sorted(region_data.items(), key=lambda x: x[1]['sales'], reverse=True)
    for region, data in sorted_regions:
        percent = (data['sales'] / total_sales * 100) if total_sales else 0
        report_lines.append(f"{region:<10}₹{data['sales']:>14,.2f}{percent:>11.2f}%{data['count']:>15}")

    report_lines.append("")

    product_data = defaultdict(lambda: {'quantity': 0, 'revenue': 0.0})
    for txn in transactions:
        name = txn.get('ProductName', 'Unknown')
        qty = int(txn.get('Quantity', 0))
        price = float(txn.get('UnitPrice', 0))
        product_data[name]['quantity'] += qty
        product_data[name]['revenue'] += qty * price

    top_products = sorted(product_data.items(), key=lambda x: x[1]['quantity'], reverse=True)[:5]

    report_lines.append("TOP 5 PRODUCTS")
    report_lines.append("-"*50)
    report_lines.append(f"{'Rank':<5}{'Product Name':<20}{'Quantity':>10}{'Revenue':>15}")
    for i, (name, data) in enumerate(top_products, 1):
        report_lines.append(f"{i:<5}{name:<20}{data['quantity']:>10}{data['revenue']:>15,.2f}")

    report_lines.append("")

    customer_data = defaultdict(lambda: {'spent': 0.0, 'count': 0})
    for txn in transactions:
        cid = txn.get('CustomerID', 'Unknown')
        qty = int(txn.get('Quantity', 0))
        price = float(txn.get('UnitPrice', 0))
        customer_data[cid]['spent'] += qty * price
        customer_data[cid]['count'] += 1

    top_customers = sorted(customer_data.items(), key=lambda x: x[1]['spent'], reverse=True)[:5]

    report_lines.append("TOP 5 CUSTOMERS")
    report_lines.append("-"*50)
    report_lines.append(f"{'Rank':<5}{'Customer ID':<15}{'Total Spent':>15}{'Order Count':>15}")
    for i, (cid, data) in enumerate(top_customers, 1):
        report_lines.append(f"{i:<5}{cid:<15}{data['spent']:>15,.2f}{data['count']:>15}")

    report_lines.append("")

    daily_data = defaultdict(lambda: {'revenue': 0.0, 'transactions': 0, 'customers': set()})
    for txn in transactions:
        date = txn.get('Date', 'N/A')
        qty = int(txn.get('Quantity', 0))
        price = float(txn.get('UnitPrice', 0))
        daily_data[date]['revenue'] += qty * price
        daily_data[date]['transactions'] += 1
        daily_data[date]['customers'].add(txn.get('CustomerID', 'Unknown'))

    report_lines.append("DAILY SALES TREND")
    report_lines.append("-"*50)
    report_lines.append(f"{'Date':<12}{'Revenue':>12}{'Transactions':>15}{'Unique Customers':>20}")
    for date in sorted(daily_data.keys()):
        data = daily_data[date]
        report_lines.append(f"{date:<12}{data['revenue']:>12,.2f}{data['transactions']:>15}{len(data['customers']):>20}")

    report_lines.append("")

    best_day = max(daily_data.items(), key=lambda x: x[1]['revenue'])[0] if daily_data else 'N/A'

    low_products = [name for name, data in product_data.items() if data['quantity'] < 10]

    avg_per_region = {region: (data['sales']/data['count'] if data['count'] else 0) for region, data in region_data.items()}

    report_lines.append("PRODUCT PERFORMANCE ANALYSIS")
    report_lines.append("-"*50)
    report_lines.append(f"Best Selling Day: {best_day}")
    report_lines.append(f"Low Performing Products (<10 units): {', '.join(low_products) if low_products else 'None'}")
    report_lines.append("Average Transaction Value per Region:")
    for region, avg in avg_per_region.items():
        report_lines.append(f"  {region}: ₹{avg:,.2f}")
    report_lines.append("")

    total_enriched = sum(1 for txn in enriched_transactions if txn.get('API_Match', False))
    total_api_attempted = len(enriched_transactions)
    success_rate = (total_enriched / total_api_attempted * 100) if total_api_attempted else 0
    failed_products = [txn.get('ProductID', 'Unknown') for txn in enriched_transactions if not txn.get('API_Match', False)]

    report_lines.append("API ENRICHMENT SUMMARY")
    report_lines.append("-"*50)
    report_lines.append(f"Total Products Enriched: {total_enriched}")
    report_lines.append(f"Success Rate: {success_rate:.2f}%")
    report_lines.append(f"Products Not Enriched: {', '.join(failed_products) if failed_products else 'None'}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))

    print(f"Sales report generated at '{output_file}'")
