"""
Fintech Optimizer

Greedy solutions for:
1. Payment Batch Scheduling
2. Investment Portfolio Selection
"""


def schedule_batches(batches):
    """
    Select the maximum number of non-overlapping payment batches.

    Greedy strategy:
    Always choose the batch that finishes earliest.

    Args:
        batches (list): List of dictionaries containing:
            - name
            - start_time
            - end_time

    Returns:
        list: Maximum set of non-overlapping batches.

    Time Complexity:
        O(n log n)
        Sorting dominates the running time.

    Space Complexity:
        O(n)
        Stores the selected batches.
    """

    sorted_batches = sorted(
        batches,
        key=lambda batch: batch["end_time"]
    )

    selected = []
    last_end_time = float("-inf")

    for batch in sorted_batches:
        if batch["start_time"] >= last_end_time:
            selected.append(batch)
            last_end_time = batch["end_time"]

    return selected


def select_portfolio(opportunities, capital):
    """
    Select investments using a greedy return-per-dollar ratio.

    Greedy strategy:
    Sort by expected_return / investment_amount
    and take the best opportunities first.

    Args:
        opportunities (list): List of dictionaries containing:
            - name
            - investment_amount
            - expected_return

        capital (int | float):
            Available investment budget.

    Returns:
        list: Selected investments.

    Time Complexity:
        O(n log n)
        Sorting dominates the running time.

    Space Complexity:
        O(n)
        Stores the selected investments.
    """

    sorted_opportunities = sorted(
        opportunities,
        key=lambda o: (
            o["expected_return"] / o["investment_amount"]
        ),
        reverse=True,
    )

    selected = []
    remaining_capital = capital

    for opportunity in sorted_opportunities:
        cost = opportunity["investment_amount"]

        if cost <= remaining_capital:
            selected.append(opportunity)
            remaining_capital -= cost

    return selected



# Sample Data

batches = [
    {"name": "A", "start_time": 0, "end_time": 6},
    {"name": "B", "start_time": 1, "end_time": 4},
    {"name": "C", "start_time": 3, "end_time": 5},
    {"name": "D", "start_time": 5, "end_time": 7},
    {"name": "E", "start_time": 6, "end_time": 8},
]


print("Scheduled Batches")
print("-" * 30)

for batch in schedule_batches(batches):
    print(batch["name"])


opportunities = [
    {
        "name": "API Integration",
        "investment_amount": 5000,
        "expected_return": 15000,
    },
    {
        "name": "Dashboard",
        "investment_amount": 3000,
        "expected_return": 7500,
    },
    {
        "name": "Mobile App",
        "investment_amount": 8000,
        "expected_return": 18000,
    },
    {
        "name": "Analytics",
        "investment_amount": 2000,
        "expected_return": 6000,
    },
]

print("\n" + "-" * 30)
print("Selected Portfolio")

portfolio = select_portfolio(opportunities, 10000)

for investment in portfolio:
    print(
        f"{investment['name']}: "
        f"cost={investment['investment_amount']}, "
        f"return={investment['expected_return']}"
    )
