"""
demo.py

Demonstrates the E-Commerce Analytics Engine.

Features demonstrated:
1. Generate 200 sample transactions
2. Build and run a processing pipeline
3. Print top 10 transactions with ranking
4. Generate a full analytics report
5. Demonstrate multi-key sorting
6. Demonstrate multiple filtering combinations
"""

from analytic_engine import (
    generate_sample_data,
    enrich_transactions,
    filter_transactions,
    sort_transactions,
    build_pipeline,
    generate_report,
)


def print_separator(title):
    """Print a formatted section separator."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():
    """Run analytics engine demonstrations."""

    print_separator("GENERATING SAMPLE DATA")

    raw_transactions = generate_sample_data(200)

    print(f"Generated {len(raw_transactions)} transaction records")

   
    print_separator("RUNNING PIPELINE")

    pipeline = build_pipeline(
        enrich_transactions,
        lambda txns: filter_transactions(
            txns,
            status="completed"
        ),
        lambda txns: sort_transactions(
            txns,
            "net_total",
            reverse=True
        ),
    )

    processed_transactions = pipeline(raw_transactions)

    print(
        f"Pipeline complete: "
        f"{len(processed_transactions)} completed transactions"
    )

    print_separator("TOP 10 TRANSACTIONS")

    for rank, txn in enumerate(
        processed_transactions[:10],
        start=1
    ):
        print(
            f"{rank:2d}. "
            f"{txn['display_id']} | "
            f"{txn['product']} | "
            f"{txn['region']} | "
            f"Net Total: ${txn['net_total']:,.2f}"
        )

   
    print_separator("FULL ANALYTICS REPORT")

    report = generate_report(
        processed_transactions,
        "revenue",
        "count",
        "avg_order",
        "by_category",
        "by_region",
        "top_customers",
        title="2024 E-Commerce Analytics Report",
        currency="USD",
        top_n=5,
        show_rank=True,
    )

    print(report)

    
    print_separator("MULTI-KEY SORT DEMO")

    multi_sorted = sort_transactions(
        processed_transactions,
        "region",
        "category",
        "net_total"
    )

    print(
        "Sorted by: region -> category -> net_total"
    )

    for txn in multi_sorted[:10]:
        print(
            f"{txn['region']:<15} "
            f"{txn['category']:<15} "
            f"${txn['net_total']:>10,.2f}"
        )

    
    print_separator("FILTER DEMONSTRATIONS")

    # Filter 1
    completed_west_africa = filter_transactions(
        processed_transactions,
        status="completed",
        region="West Africa"
    )

    print(
        f"Completed + West Africa: "
        f"{len(completed_west_africa)} transactions"
    )

    # Filter 2
    electronics_large_orders = filter_transactions(
        processed_transactions,
        category="Electronics",
        min_total=1000
    )

    print(
        f"Electronics + Net Total >= 1000: "
        f"{len(electronics_large_orders)} transactions"
    )

    # Filter 3
    premium_west_africa = filter_transactions(
        processed_transactions,
        category="Electronics",
        region="West Africa",
        min_total=2000
    )

    print(
        f"Electronics + West Africa + "
        f"Net Total >= 2000: "
        f"{len(premium_west_africa)} transactions"
    )

    print_separator("DEMO COMPLETE")


if __name__ == "__main__":
    main()
