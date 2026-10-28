"""
    A transaction reporting tool that sorts transactions using
    manual algorithms and Python's built-in sort, benchmarks their
    performance, and helps generate business insights.
"""

import time

def bubble_sort_transactions(transactions, key):
    """Sorts a list of transaction dicts in ascending order by a given key(e.g. 'amount').

    Args: 
        transactions: the list to sort.
        key: use to sort in ascending order.
        
    Time complexity: O(n²) average and worst case.
    Space complexity: O(1) — sorts in place.
    """
    n = len(transactions)
    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            if transactions[j][key] > transactions[j + 1][key]:
                transactions[j], transactions[j + 1] = (transactions[j + 1],transactions[j])
                swapped = True
        if not swapped:
                break


def selection_sort_transaction(transactions, key):
    """
    Sort a list in ascending order using selection sort.

    Modifies the list in place.

    Time complexity: O(n²) in all cases — always scans the full unsorted portion.
    Space complexity: O(1)
    """
    n = len(transactions)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if transactions[j][key] < transactions[min_index][key]:
                min_index = j
        transactions[i], transactions[min_index] = transactions[min_index], transactions[i]


def benchmark_sorts(transactions):
    """
    Compare the execution time of three sorting strategies.

    Sorts transactions by amount in ascending order.

    Time complexity:
        Bubble Sort: O(n^2) average and worst case.
        Selection Sort: O(n^2).
        Built-in Sort: O(n log n) average case.

    Space complexity:
        Depends on the sorting method and the copies made.
    """
    # Create separate copies so each method gets the same data.
    bubble_data = transactions.copy()
    selection_data = transactions.copy()
    builtin_data = transactions.copy()

    # Benchmark Bubble Sort.
    start = time.perf_counter()
    bubble_sort_transactions(bubble_data, "amount")
    bubble_time = time.perf_counter() - start

    # Benchmark Selection Sort.
    start = time.perf_counter()
    selection_sort_transaction(selection_data, "amount")
    selection_time = time.perf_counter() - start

    # Benchmark Python's built-in sort.
    start = time.perf_counter()
    sorted(builtin_data, key=lambda transaction: transaction["amount"])
    builtin_time = time.perf_counter() - start

    # Display the results.
    print(f"Bubble Sort:    {bubble_time:.6f} seconds")
    print(f"Selection Sort: {selection_time:.6f} seconds")
    print(f"Built-in Sort:  {builtin_time:.6f} seconds")


def top_n_transactions(transactions, n, key="amount"):
    """
    Return the top n transactions based on the given key.

    Args:
        transactions: A list of transaction dictionaries.
        n: The number of top transactions to return.
        key: The dictionary field used for ranking.

    Returns:
        A list containing the top n transactions.

    Time complexity:
        O(m log m), where m is the number of transactions.

    Space complexity:
        O(m), where m is the number of transactions.
    """
    if n <= 0:
        return []

    sorted_transactions = sorted(
        transactions,
        key=lambda transaction: transaction[key],
        reverse=True,
    )

    return sorted_transactions[:n]


def transactions_by_category(transactions):
    """
    Group transactions by category and sort each group by amount.

    Args:
        transactions: A list of transaction dictionaries.

    Returns:
        A dictionary mapping each category to its sorted transactions.

    Time complexity:
        O(n log n), where n is the number of transactions.

    Space complexity:
        O(n), where n is the number of transactions.
    """
    categories = {}

    # Group transactions by category.
    for transaction in transactions:
        category = transaction["category"]

        if category not in categories:
            categories[category] = []

        categories[category].append(transaction)

    # Sort transactions within each category.
    for category in categories:
        categories[category] = sorted(
            categories[category],
            key=lambda transaction: transaction["amount"],
        )

    return categories


def display_results(transactions):
    """
    Display the results of all transaction sorting functions.
    """

    print("\n" + "-" * 35)
    print("       TRANSACTION MANAGEMENT SYSTEM")
    print("-" * 35)

    # 1. Display original transactions
    print("\n1. ORIGINAL TRANSACTIONS")
    print()

    for transaction in transactions:
        print(
            f"Name: {transaction['name']:<10} "
            f"Category: {transaction['category']:<12} "
            f"Amount: {transaction['amount']:,.2f}"
        )

    # 2. Bubble Sort
    print("\n2. BUBBLE SORT (Amount: Lowest to Highest)")
    print()

    bubble_data = transactions.copy()
    bubble_sort_transactions(bubble_data, "amount")

    for transaction in bubble_data:
        print(
            f"{transaction['name']:<10} "
            f"{transaction['amount']:,.2f}"
        )

    # 3. Selection Sort
    print("\n3. SELECTION SORT (Amount: Lowest to Highest)")
    print()

    selection_data = transactions.copy()
    selection_sort_transaction(selection_data, "amount")

    for transaction in selection_data:
        print(
            f"{transaction['name']:<10} "
            f"{transaction['amount']:,.2f}"
        )

    # 4. Built-in Sort
    print("\n4. BUILT-IN SORT (Amount: Lowest to Highest)")
    print()

    builtin_data = sorted(
        transactions,
        key=lambda transaction: transaction["amount"],
    )

    for transaction in builtin_data:
        print(
            f"{transaction['name']:<10} "
            f"{transaction['amount']:,.2f}"
        )

    # 5. Top 3 Transactions
    print("\n5. TOP 3 TRANSACTIONS (Highest Amounts)")
    print()

    top_transactions = top_n_transactions(transactions, 3)

    for transaction in top_transactions:
        print(
            f"{transaction['name']:<10} "
            f"{transaction['amount']:,.2f}"
        )

    # 6. Transactions Grouped by Category
    print("\n6. TRANSACTIONS BY CATEGORY")
    print()

    grouped_transactions = transactions_by_category(transactions)

    for category, items in grouped_transactions.items():
        print(f"\nCategory: {category}")

        for transaction in items:
            print(
                f"  {transaction['name']:<10} "
                f"{transaction['amount']:,.2f}"
            )

    print()
    print("ALL DISPLAY OPERATIONS COMPLETED")
    print()


if __name__ == "__main__":
    transactions = [
        {
            "name": "Food",
            "category": "Shopping",
            "amount": 5000,
        },
        {
            "name": "Bus",
            "category": "Transport",
            "amount": 1500,
        },
        {
            "name": "Rice",
            "category": "Shopping",
            "amount": 2000,
        },
        {
            "name": "Taxi",
            "category": "Transport",
            "amount": 3000,
        },
        {
            "name": "Bread",
            "category": "Shopping",
            "amount": 1000,
        },
    ]

    display_results(transactions)
