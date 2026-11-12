"""Demonstrate the e-commerce analytics engine."""

from analytic_engine import (
    build_pipeline,
    enrich_transactions,
    filter_transactions,
    generate_report,
    generate_sample_data,
    sort_transactions,
)


def print_separator(title: str) -> None:
    """Print a clearly labeled section heading.

    Args:
        title: Text to display between separator lines.
    """
    print(f"\n{'=' * 70}\n{title}\n{'=' * 70}")


def main() -> None:
    """Run the required pipeline, reporting, sorting, and filtering demos."""
    print_separator("GENERATING SAMPLE DATA")
    raw_transactions = generate_sample_data(200)
    print(f"Generated {len(raw_transactions)} transaction records")

    print_separator("RUNNING PIPELINE")
    pipeline = build_pipeline(
        enrich_transactions,
        lambda txns: filter_transactions(txns, status="completed"),
        lambda txns: sort_transactions(txns, "net_total", reverse=True),
    )
    processed = pipeline(raw_transactions)
    print(f"Pipeline complete: {len(processed)} completed transactions")

    print_separator("TOP 10 TRANSACTIONS")
    for rank, txn in enumerate(processed[:10], start=1):
        print(
            f"{rank:2d}. {txn['display_id']} | {txn['product']} | "
            f"{txn['region']} | Net Total: ${txn['net_total']:,.2f}"
        )

    print_separator("FULL ANALYTICS REPORT")
    print(generate_report(
        processed,
        "revenue", "count", "avg_order", "by_category", "by_region", "top_customers",
        title="2024 E-Commerce Analytics Report",
        currency="USD",
        top_n=5,
        show_rank=True,
    ))

    print_separator("MULTI-KEY SORT DEMO")
    multi_sorted = sort_transactions(processed, "region", "category", "net_total")
    print("Sorted by: region -> category -> net_total")
    for txn in multi_sorted[:10]:
        print(f"{txn['region']:<15} {txn['category']:<15} ${txn['net_total']:>10,.2f}")

    print_separator("FILTER DEMONSTRATIONS")
    examples = [
        ("Completed + West Africa", {"status": "completed", "region": "West Africa"}),
        ("Electronics", {"category": "Electronics"}),
        ("Electronics + West Africa", {"category": "Electronics", "region": "West Africa"}),
        ("Orders from $1,000 to $5,000", {"min_total": 1000, "max_total": 5000}),
    ]
    for label, criteria in examples:
        result = filter_transactions(processed, **criteria)
        print(f"{label}: {len(result)} transactions")

    print_separator("DEMO COMPLETE")


if __name__ == "__main__":
    main()
