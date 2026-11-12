""" 
    Analytics Engine
A flexible engine that process raw transaction data exported
from an e-commerce company database using composable pipeline of functions.
"""

from functools import reduce
import random
from datetime import datetime, timedelta



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

def enrich_transactions(transactions):
    """Uses map to add computed fields to every record.
    Args:
        transactions:List of transaction dicts
        discount_pct: the percentage discount of every sales.
    Returns: 
        New list where each record has total, discount, display id, and net_total. """
    def enrich_record(record):
        gross_total = record["quantity"] * record["unit_price"]
        discount_amount = record["quantity"] * record["unit_price"] * record["discount_pct"] / 100
        net_total = (
    record["quantity"]
    * record["unit_price"]
    - discount_amount
)
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
    lambda total, tx:
        total + tx["net_total"],
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
        current_collect["total_revenue"] += record["net_total"]
        current_collect["average_order_value"] += record["net_total"]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

        return collect
    grouped = reduce(collector, transactions, {})

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
    return run_pipeline     


def generate_report(
    transactions,
    *metrics,
    title="Report",
    **options
):
    """
    Generate a configurable analytics report.

    Args:
        transactions (list):
            Enriched transaction records.

        *metrics:
            Metrics to include:
            revenue
            count
            avg_order
            by_category
            by_region
            top_customers

        title (str):
            Report title.

        **options:
            top_n (int):
                Number of top customers.

            currency (str):
                Currency symbol/code.

            show_rank (bool):
                Show ranking numbers.

    Returns:
        str:
            Formatted multi-line report.
    """

    currency = options.get("currency", "USD")
    top_n = options.get("top_n", 5)
    show_rank = options.get("show_rank", True)

    lines = []

    lines.append(title)
    lines.append("=" * len(title))
    lines.append("")

    #
    # Revenue
    #
    if "revenue" in metrics:

        revenue = total_revenue(transactions)

        lines.append("REVENUE")
        lines.append("-" * 40)
        lines.append(
            f"Total Revenue: "
            f"{currency} {revenue:,.2f}"
        )
        lines.append("")

    #
    # Count
    #
    if "count" in metrics:

        lines.append("TRANSACTION COUNT")
        lines.append("-" * 40)
        lines.append(
            f"Transactions: "
            f"{len(transactions)}"
        )
        lines.append("")

    #
    # Average Order
    #
    if "avg_order" in metrics:

        avg_order = 0

        if transactions:

            avg_order = (
                total_revenue(transactions)
                /
                len(transactions)
            )

        lines.append("AVERAGE ORDER VALUE")
        lines.append("-" * 40)

        lines.append(
            f"Average Order: "
            f"{currency} "
            f"{avg_order:,.2f}"
        )

        lines.append("")

    #
    # By Category
    #
    if "by_category" in metrics:

        lines.append("CATEGORY BREAKDOWN")
        lines.append("-" * 40)

        summary = summarize_by(
            transactions,
            "category"
        )

        for category, stats in summary.items():

            lines.append(
                f"{category}"
            )

            lines.append(
                f"  Count: "
                f"{stats['count']}"
            )

            lines.append(
                f"  Revenue: "
                f"{currency} "
                f"{stats['total_revenue']:,.2f}"
            )

            lines.append(
                f"  Avg Order: "
                f"{currency} "
                f"{stats['avg_order_value']:,.2f}"
            )

            lines.append(
                f"  Top Product: "
                f"{stats['top_product']}"
            )

            lines.append("")

    #
    # By Region
    #
    if "by_region" in metrics:

        lines.append("REGIONAL BREAKDOWN")
        lines.append("-" * 40)

        summary = summarize_by(
            transactions,
            "region"
        )

        for region, stats in summary.items():

            lines.append(
                f"{region}"
            )

            lines.append(
                f"  Count: "
                f"{stats['count']}"
            )

            lines.append(
                f"  Revenue: "
                f"{currency} "
                f"{stats['total_revenue']:,.2f}"
            )

            lines.append(
                f"  Avg Order: "
                f"{currency} "
                f"{stats['avg_order_value']:,.2f}"
            )

            lines.append(
                f"  Top Product: "
                f"{stats['top_product']}"
            )

            lines.append("")

    #
    # Top Customers
    #
    if "top_customers" in metrics:

        customer_totals ={}

        for tx in transactions:

            customer_totals[
                tx["customer"]
            ] += tx["net_total"]

        ranking = sorted(
            customer_totals.items(),
            key=lambda item: item[1],
            reverse=True
        )

        lines.append("TOP CUSTOMERS")
        lines.append("-" * 40)

        for position, (
            customer,
            revenue
        ) in enumerate(
            ranking[:top_n],
            start=1
        ):

            if show_rank:

                lines.append(
                    f"{position}. "
                    f"{customer} "
                    f"({currency} "
                    f"{revenue:,.2f})"
                )

            else:

                lines.append(
                    f"{customer} "
                    f"({currency} "
                    f"{revenue:,.2f})"
                )

        lines.append("")

    return "\n".join(lines)




def generate_sample_data(n, **overrides):
    """
    Generate random e-commerce transaction records.

    Uses enumerate() to create sequential transaction IDs and zip()
    to pair randomly selected customers with products.

    Args:
        n (int): Number of transaction records to generate.
        **overrides: Optional field values that should override
            generated values for all records.

    Returns:
        list[dict]: List of transaction records.
    """
    customers = [
        "Ada Lovelace",
        "Alan Turing",
        "Grace Hopper",
        "Katherine Johnson",
        "Tim Berners-Lee",
        "Margaret Hamilton",
        "Linus Torvalds",
        "James Gosling",
        "Guido van Rossum",
        "Dennis Ritchie"
    ]

    products = [
        ("Laptop Pro", "Electronics"),
        ("Wireless Mouse", "Electronics"),
        ("Office Chair", "Furniture"),
        ("Standing Desk", "Furniture"),
        ("Python Handbook", "Books"),
        ("Data Science Guide", "Books"),
        ("Smartphone X", "Electronics"),
        ("USB-C Hub", "Electronics"),
        ("Monitor 27\"", "Electronics"),
        ("Notebook Pack", "Stationery")
    ]

    statuses = ["completed", "pending", "cancelled"]
    regions = [
        "West Africa",
        "East Africa",
        "North America",
        "Europe",
        "Asia Pacific"
    ]

    # Randomly pair customers and products using zip()
    customer_choices = random.choices(customers, k=n)
    product_choices = random.choices(products, k=n)

    paired_records = zip(customer_choices, product_choices)

    transactions = []

    for index, (customer, (product, category)) in enumerate(
        paired_records,
        start=1
    ):
        record = {
            "id": f"TXN-{index:03d}",
            "customer": customer,
            "product": product,
            "category": category,
            "quantity": random.randint(1, 10),
            "unit_price": round(random.uniform(10, 5000), 2),
            "discount_pct": random.choice([0, 5, 10, 15, 20]),
            "status": random.choice(statuses),
            "date": (
                datetime(2024, 1, 1)
                + timedelta(days=random.randint(0, 364))
            ).strftime("%Y-%m-%d"),
            "region": random.choice(regions)
        }

        # Apply user-specified overrides
        record.update(overrides)

        transactions.append(record)

    return transactions
