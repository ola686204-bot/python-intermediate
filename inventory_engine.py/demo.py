"""
demo.py

Demonstrates the inventory processing features:

1. Generate 50+ inventory records
2. Enrich records and build SKU index
3. Paginate inventory
4. Group inventory by region
5. Use cached category statistics
6. Compose threshold filters
7. Chain low-stock records from multiple sources
"""

import random

from inventory_engine import (
    enrich_inventory,
    build_sku_index,
    paginate_inventory,
    group_by_region,
    freeze_records,
    cached_category_stats,
    make_threshold_filter,
    chain_low_stock_sources,
)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

CATEGORIES = [
    "Electronics",
    "Stationery",
    "Furniture",
    "Accessories",
]

REGIONS = [
    "North",
    "South",
    "West",
]

SUPPLIERS = [
    "TechWorld",
    "Prime Supplies",
    "Global Traders",
    "MegaStore",
    "Elite Distribution",
]


# ---------------------------------------------------------
# Generate sample inventory
# ---------------------------------------------------------

def create_sample_inventory():
    """Create at least 50 sample inventory records."""

    records = []

    random.seed(42)

    for number in range(1, 61):
        category = random.choice(CATEGORIES)
        region = random.choice(REGIONS)
        supplier = random.choice(SUPPLIERS)
        unit_cost = round(random.uniform(10, 500), 2)

        record = {
            "sku": f"SKU-{number:03d}",
            "name": f"Product {number}",
            "category": category,
            "subcategory": "General",
            "region": region,
            "store_id": f"STORE-{(number % 5) + 1:03d}",
            "supplier": supplier,
            "stock": random.randint(1, 100),
            "reorder_point": random.randint(5, 20),
            "unit_cost": unit_cost,
            "unit_price": round(unit_cost * random.uniform(1.1, 2.0), 2),
            "last_sold_days_ago": random.randint(1, 30),
        }

        records.append(record)

    return records


# ---------------------------------------------------------
# Main demonstration
# ---------------------------------------------------------

def main():
    """Run all inventory demonstrations."""

    records = create_sample_inventory()

    print("\n1. GENERATED INVENTORY")
    print("-" * 60)
    print(f"Total records generated: {len(records)}")

    print("\nSample records:")

    for record in records[:5]:
        print(record)

    # -----------------------------------------------------
    # 2. Enrich records
    # -----------------------------------------------------

    print("\n2. ENRICH RECORDS")
    print("-" * 60)

    enriched_records = enrich_inventory(records)

    print(f"Enriched records: {len(enriched_records)}")

    for record in enriched_records[:3]:
        print(record)

    # -----------------------------------------------------
    # 3. Build SKU index
    # -----------------------------------------------------

    print("\n3. BUILD SKU INDEX")
    print("-" * 60)

    sku_index = build_sku_index(enriched_records)

    print(f"SKU index contains {len(sku_index)} records")

    first_sku = next(iter(sku_index))

    print("\nExample SKU:")
    print(first_sku)

    print("\nRecord belonging to that SKU:")
    print(sku_index[first_sku])

    # -----------------------------------------------------
    # 4. Demonstrate pagination
    # -----------------------------------------------------

    print("\n4. PAGINATION")
    print("-" * 60)

    page_size = 10

    pages = paginate_inventory(enriched_records, page_size=page_size)
    page_one = next(pages)
    page_two = next(pages)

    print("\n--- PAGE 1 ---")

    for record in page_one:
        print(record)

    print("\n--- PAGE 2 ---")

    for record in page_two:
        print(record)

    # -----------------------------------------------------
    # 5. Group by region
    # -----------------------------------------------------

    print("\n5. GROUP BY REGION")
    print("-" * 60)

    grouped = group_by_region(enriched_records)

    for region, region_records in grouped.items():
        print(f"{region}: {len(region_records)} records")

    # -----------------------------------------------------
    # 6. Cached category statistics
    # -----------------------------------------------------

    print("\n6. CACHED CATEGORY STATISTICS")
    print("-" * 60)

    category = "Electronics"

    print(f"Calculating statistics for: {category}")

    first_result = cached_category_stats(
        category,
        freeze_records(enriched_records),
    )

    print("\nFirst call:")
    print(first_result)

    second_result = cached_category_stats(
        category,
        freeze_records(enriched_records),
    )

    print("\nSecond call:")
    print(second_result)

    print("\nCache information:")

    print(cached_category_stats.cache_info())

    # -----------------------------------------------------
    # 7. Threshold filters
    # -----------------------------------------------------

    print("\n7. COMPOSED THRESHOLD FILTERS")
    print("-" * 60)

    # First filter:
    # stock >= 20
    quantity_filter = make_threshold_filter(
        "stock",
        operator="gte",
        value=20,
    )

    # Second filter:
    # stock <= 70
    upper_quantity_filter = make_threshold_filter(
        "stock",
        operator="lte",
        value=70,
    )

    filtered_records = list(
        upper_quantity_filter(quantity_filter(enriched_records))
    )

    print("First threshold: stock >= 20")
    print("Second threshold: stock <= 70")

    print(
        f"\nRecords satisfying both thresholds: "
        f"{len(filtered_records)}"
    )

    print("\nMatching records:")

    for record in filtered_records[:10]:
        print(record)

    # -----------------------------------------------------
    # 8. Chain low-stock sources
    # -----------------------------------------------------

    print("\n8. CHAIN LOW-STOCK SOURCES")
    print("-" * 60)

    # Split the inventory into three separate sources.

    source_one = enriched_records[:20]
    source_two = enriched_records[20:40]
    source_three = enriched_records[40:60]

    print(f"Source 1 records: {len(source_one)}")
    print(f"Source 2 records: {len(source_two)}")
    print(f"Source 3 records: {len(source_three)}")

    # Chain the three sources together and find low-stock items.

    low_stock_records = chain_low_stock_sources(
        source_one,
        source_two,
        source_three,
    )

    print(
        f"\nLow-stock records found: "
        f"{len(low_stock_records)}"
    )

    for record in low_stock_records[:15]:
        print(record)

    # -----------------------------------------------------
    # Finished
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
