""" Transaction Search Engine.
A transaction dataset that iplements both linear and binary search,
benchmarks their performance, and selects the appropriate algorithm based on data state."""

import random
import time

def generate_transactions(n):
    """
        Generate n random transactions.
    
        Args: 
            n (int): Number of records.
    
        Returns:
            list[dict]: Transaction dataset.
        """
    return [
        {
            'id': i,
            'ref': f'TXN-{i:06d}',
            'amount': random.randint(100, 100000),
            'category': random.choice(['transfer', 'payment', 'withdrawal', 'deposit'])
        }
        for i in range(n)
    ]


def linear_search_by_id(transactions, target_id):
    """search a transaction by id.
    Args:
        transaction: the transaction to search by id.
        target_id: the transaction search for.
    Returns:
        the matching transaction dict or None.
    Time complexity: O(n) — worst case scans every element.
    Space complexity: O(1) — no additional data structures.
    """
    for transaction in transactions:
        if transaction ['id'] == target_id:
            return transaction
    return None


def binary_search_by_amount(sorted_transactions, target_amount):
    """Search transaction by amount.
    Args:
        sorted transactions:A sorted list of comparable transactions.
        target_amount: the value to search for.
    Returns:
        The index of target if found, otherwise -1.
    Time complexity: O(log n)
    Space complexity: O(1)
          """
    left = 0
    right = len(sorted_transactions) - 1

    while left <= right:
        mid = (left + right) // 2

        amount = sorted_transactions[mid]["amount"]

        if amount == target_amount:
            return mid

        if amount < target_amount:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def smart_search(transactions, target_id):
    """ Automatically selects the best search strategy.
    
        If transactions are sorted by ID:
            Uses binary search.
    
        Otherwise:
            Uses linear search.
    
        Time Complexity:
            Sorted:O(log n
    
            Unsorted:O(n)

        Space Complexity:
            O(1)
    Args:
        transactions (list): Transaction dataset.
        target_id(int):ID to search for.
    Returns:
        dict | none."""
    is_sorted = all(
            transactions[i]["id"] <= transactions[i + 1]["id"]
            for i in range(len(transactions) - 1)
        )
    
    if not is_sorted:
        print("[SMART SEARCH] Using Linear Search")
        return linear_search_by_id(
            transactions,
            target_id,
        )
    
    print("[SMART SEARCH] Using Binary Search")
    
    left = 0
    right = len(transactions) - 1
    
    while left <= right:
        mid = (left + right) // 2
    
        current_id = transactions[mid]["id"]
    
        if current_id == target_id:
            return transactions[mid]
    
        if current_id < target_id:
            left = mid + 1
        else:
            right = mid - 1
    
    return None


def benchmark(sort_fn, data):
    """
    Benchmark search algorithms.

    Measures execution time for:
    - Linear Search
    - Binary Search

    Args:
        sort_fn (callable):
            Function used to sort by amount.

        data (list):
            Transaction dataset.
    """
    print("\n" + "=" * 50)
    print("BENCHMARK RESULTS")
    print("=" * 50)

    target_id = data[-1]["id"]

    start = time.perf_counter()

    linear_search_by_id(
        data,
        target_id,
    )

    linear_elapsed = time.perf_counter() - start

    sorted_by_amount = sort_fn(
        data,
        key=lambda x: x["amount"]
    )

    target_amount = sorted_by_amount[
        len(sorted_by_amount) // 2
    ]["amount"]

    start = time.perf_counter()

    binary_search_by_amount(
        sorted_by_amount,
        target_amount,
    )

    binary_elapsed = time.perf_counter() - start

    print(
        f"Linear Search: "
        f"{linear_elapsed:.8f} seconds"
    )

    print(
        f"Binary Search: "
        f"{binary_elapsed:.8f} seconds"
    )

    print("\nComplexity Analysis")

    print(
        "Linear Search -> O(n)"
    )

    print(
        "Binary Search -> O(log n)"
    )

    if binary_elapsed < linear_elapsed:
        print(
            "Binary search is faster because "
            "it halves the search space each step."
        )
    else:
        print(
            "Linear search performed similarly "
            "for this dataset."
        )
    
    
    # ==================================
    # Demonstration
    # ==================================
    
if __name__ == "__main__":

    transactions = generate_transactions(10_000)

    print("\nLINEAR SEARCH EXAMPLE")
    result = linear_search_by_id(
        transactions,
        5000,
    )
    print(result)

    print("\nBINARY SEARCH EXAMPLE")

    sorted_transactions = sorted(
        transactions,
        key=lambda x: x["amount"]
    )

    amount_target = sorted_transactions[2500]["amount"]

    index = binary_search_by_amount(
        sorted_transactions,
        amount_target,
    )

    print("Found at index:", index)

    print("\nSMART SEARCH EXAMPLE")

    result = smart_search(
        transactions,
        7000,
    )

    print(result)

    benchmark(
        sorted,
        transactions,
    )


