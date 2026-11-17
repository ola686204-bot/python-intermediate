import itertools
from itertools import chain, islice
from operator import itemgetter
from functools import lru_cache, partial, reduce
import operator as operator_module


record = {
    'sku': 'ELEC-001',
    'name': 'Laptop Pro 15',
    'category': 'Electronics',
    'subcategory': 'Laptops',
    'region': 'West Africa',
    'store_id': 'WA-003',
    'stock': 12,
    'reorder_point': 5,
    'unit_cost': 450.00,
    'unit_price': 899.99,
    'last_sold_days_ago': 3,
    'supplier': 'TechSupply Ltd'
}

def enrich_inventory(records):
    """Uses a list comprehension to add to every record.
    Args:
        records: list of dicts.
    Returns:
        return a new list of dicts.
    """
    return [
        {
            **item,
            "margin": item["unit_price"] - item["unit_cost"],
            "margin_pct": round(
                (
                    (item["unit_price"] - item["unit_cost"])
                    / item["unit_price"]
                ) * 100,
                2,
            ),
            "inventory_value": item["stock"] * item["unit_cost"],
            "needs_reorder": item["stock"] <= item["reorder_point"],
            "days_of_stock": (
                item["stock"]
                / max(1, 30 / max(1, item["last_sold_days_ago"]))
            ),
        }
        for item in records
    ]


def build_sku_index(records):
    """Use a dict comprehension to return sku record."""
    return {record["sku"]: record for record in records}


def get_unique_suppliers(records):
    """Use a set comprehension to return all unique supplier names."""
    return {record["supplier"] for record in records}


def build_category_matrix(records):
    """Use a nested dict comprehension to return a category and a sub category."""
    return {
        category: {
            subcategory: [
                record
                for record in records
                if record["category"] == category
                and record["subcategory"] == subcategory
            ]
            for subcategory in {
                record["subcategory"]
                for record in records
                if record["category"] == category
            }
        }
        for category in {record["category"] for record in records}
    }


def all_reorder_combination(records, r=2):
    """Use itertools.combinations to return all combinations of r items that all need reordering."""
    reorder_items = [record for record in records if record["needs_reorder"]]
    return itertools.combinations(reorder_items, r)


def generate_restock_orders(records, suppliers):
    """Uses itertools.product to generate all possible supplier item pairings for restock consideration."""
    reorder_items = [record for record in records if record["needs_reorder"]]
    return itertools.product(reorder_items, suppliers)


def paginate_inventory(records, page_size=20):
    """Uses itertools.islice to yield pages of records as a generator."""
    iterator = iter(records)
    while True:
        page = list(islice(iterator, page_size))
        if not page:
            return
        yield page


def group_by_region(records):
    """Uses itertools.groupby to return a dict of regions."""
    sorted_regions = sorted(records, key=itemgetter("region"))
    return {
        region: list(items)
        for region, items in itertools.groupby(sorted_regions, key=itemgetter("region"))
    }


def chain_low_stock_sources(*sources):
    """Return records that need reordering from multiple sources."""
    return [
        record
        for record in chain(*sources)
        if record["needs_reorder"] is True
    ]

def freeze_records(records):
    """Convert a list of dicts into a hashable tuple."""
    return tuple(frozenset(record.items()) for record in records)

@lru_cache(maxsize=64)
def cached_category_stats(category, records_tuple):
    """Calculate and cache category statistics."""
    records = [dict(record) for record in records_tuple]
    category_records = [record for record in records if record["category"] == category]
    return {
        "count": len(category_records),
        "total_value": sum(
    record.get("inventory_value", 0)
    for record in category_records
),
        "avg_margin_pct": (
            sum(record.get("margin_pct", 0) for record in category_records)
            / len(category_records)
            if category_records
            else 0
        ),
        "items_needing_reorder": [
            record for record in category_records if record["needs_reorder"]
        ],
    }

def _filter_records(records, field, comparison, value):
    """Filter records using a comparison operation."""

    return (
        record for record in records
        if comparison(record.get(field), value)
    )


def make_threshold_filter(field, *, operator='gte', value):
    """Create a reusable threshold filter."""

    operators = {
        "gte": operator_module.ge,
        "lte": operator_module.le,
        "eq": operator_module.eq,
        "gt": operator_module.gt,
        "lt": operator_module.lt
    }

    if operator not in operators:
        raise ValueError(f"Unsupported operator: {operator}")

    return partial(
        _filter_records,
        field=field,
        comparison=operators[operator],
        value=value
    )


# --------------------------------------------------
# 4. COMPUTE TOTALS USING REDUCE
# --------------------------------------------------

def compute_totals(records):
    """Calculate inventory totals using reduce."""

    initial = {
        "total_inventory_value": 0,
        "total_items": 0,
        "items_needing_reorder": 0,
        "categories_seen": set()
    }

    def accumulator(totals, record):
        totals["total_inventory_value"] += record.get("inventory_valueq", 0)

        totals["total_items"] += 1

        if record.get("needs_reorder") is True:
            totals["items_needing_reorder"] += 1

        if record.get("category"):
            totals["categories_seen"].add(record["category"])

        return totals

    return reduce(accumulator, records, initial)

