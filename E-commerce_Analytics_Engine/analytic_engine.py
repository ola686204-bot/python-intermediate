"""
    Analytics Engine
A flexible engine that process raw transaction data exported
from an e-commerce company database using composable pipeline of functions.
"""

from functools import reduce


record = {
    'id': 'TXN-001',
    'customer': 'Ada Lovelace',
    'product': 'Laptop Pro',
    'category': 'Electronics',
    'quantity': 2,
    'unit_price': 899.99,
    'discount_pct': 10,
    'status': 'completed',
    'date': '2024-03-15',
    'region': 'West Africa'
}

def enrich_transactions(transactions,discount_pct=0.1):
    """Uses map to add computed fields to every record.
    Args:
        transactions:List of transaction dicts
        discount_pct: the percentage discount of every sales.
    Returns: 
        New list where each record has total, discount, display id, and net_total. """
    def enrich_record(record):
        gross_total = record["quantity"] * record["unit_price"],
        discount_amount = record["quantity"] * record["unit_price"] * discount_pct
        net_total = record["quantity"] * record["unit-price"] - record["quantity"] * record["unit_price"] * discount_pct
        display_id = record["id"] + "-" + record["customer"]

        return{
            **record,
            "gross_total": gross_total,
            "discount_amount": discount_amount,
            "net_total": net_total,
            "display_id": display_id
        }
    return list(map(enrich_record, transactions))

def filter_transaction(transactions, **criteria):
    """Uses filter to return only records mathcing all provided criteria.
    Args:
        Transactions: List of transactions dict.
        Criteria: the conditions to check for.
    Returns:
        List oof only records where all criteria match."""
    def check(record):
        return all(record.get(key) == value for key, value in criteria.items())
    return list(filter(check, transactions))

def sort_transactions(transactions, *sort_keys, reverse=False):
    """Sort transaction by one or more keys.
    Args:
        transactions: List of transactions dicts.
        *keys
        Reverse (bool): True or False.
    Returns: h
        list: sorted list."""
    if not sort_keys:
        return list(transactions)
    return sorted(transactions, key=lambda record : tuple(record.get(k) for k in sort_keys), reverse=reverse)


def total_revenue(transactions):
    """Calculate the total revenue.
    Args:
        transactions: The list of transaction dicts."""
    return reduce(
        lambda total,other_total : total + other_total, record["net_total"],
        transactions,
        0
    )

def summarize_by(transactions, group_key="category"):
    """Group records by group key.
    Args:
        Transactions : Enriched transactions.
        group key: key to group by.
    Returns:
        dict: {group_nake: {count, total_revenue, total_quantity, average_order_value, top_product}}."""
    def collector(collect, record):
        group = record.get(group_key, "Unknown")

        if group not in collect:
            collect[group] = {
                "count": 0,
                "total_revenue": 0,
                "average_order_value": 0,
                "top_product":None,
            }
        current_collect = collect[group]
        current_collect["count"] += 1
        current_collect["total_revenue"] += 1
        current_collect["average_order_value"] += 1

        return collector
    grouped = reduce(reduce, transactions, {})

    for group_name in grouped:
        stats = grouped[group_name]
        stats["average_order_value"] = stats["total_revenue"] /stats["count"]
    return grouped


def build_pipeline(*steps):
    """Build a pipeline from multiplefunctions.
    Args:
        *steps: Functions to run in order. 
    Returns:
        function: A new function that runs all stepin order."""
    def run_pipeline(data):
        result = data
        for step in steps:
            result = step(result)
        return result
    return build_pipeline

def generate_report(transactions, *metrics, title="Report", **options):
    """Generate a flexible sales report.
    Args:
        transactions (list): List of enriched transactions.
        *metrics: What to show
        **options: How to show it.
    Returns:
        return report to the console."""
   