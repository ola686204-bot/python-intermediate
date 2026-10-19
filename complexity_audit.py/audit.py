""" Complexity Audit."""

# Function 1
def find_large_transactions(transactions, threshold):
    large =[]
    for tx in transactions:
        if tx['amount'] > threshold:
            large.append(tx)
        return large

# Audited Function 1
def find_large_transactions(transactions, threshold):
    """Finds transactions that exceed a specified threshold.
    Args:
        transactions: list of transaction dicts, each with  a 'threshold' key.
        threshold: The transaction 'threshold' to look for.
    Returns:
        The matching transaction dict, or Name if not found
    Time Complexity: O(n) where n is the number of transactions.
    Space complexity: O(1) no addditional data structure used.
        """
    large =[]
    for tx in transactions:
        if tx['amount'] > threshold:
            large.append(tx)
        return large
    
# Fuunction 2
def has_duplicate_references(transactions):
    for i in range(len(transactions)):
        for j in range(len(transactions)):
            if i != j and transactions[i]['ref'] == transactions[j]['ref']:
                return True
    return False



# Audited Function 2
def has_duplicate_references(transactions):
    """Checks for duplicate transaction references.
    Args:
        transactions: list of transaction dicts, each with a 'ref' key.
    Returns:
        True if a duplicate is found, False otherwise.
    Time Complexity: O(n^2) where n is the number of transactions.
    Space Complexity: O(1) no additional data structures used.
    """
    for i in range(len(transactions)):
        for j in range(len(transactions)):
            if i != j and transactions[i]['ref'] == transactions[j]['ref']:
                return True
    return False
# Improved Function 2
def has_duplicate_reference(transactions):
    """
    Checks whether any transaction reference appears more than once.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    seen_refs = set()

    for transaction in transactions:
        ref = transaction["ref"]

        if ref in seen_refs:
            return True

        seen_refs.add(ref)

    return False
# Summary of Function 2

# Inefficiency in the original implementation:
# The function uses nested loops, causing O(n²) time complexity.
# For large transaction lists, the number of comparisons grows rapidly,
# making the function significantly slower. Using a set allows duplicate
# detection in a single pass, reducing the time complexity to O(n).



# Function 3
def get_transaction_by_id(transactions, target_id):
    for tx in transactions:
        if tx['id'] == target_id:
            return tx
    return None

# Audited Function 3
def get_transaction_by_id(transactions, target_id):
    """Retrieves a transaction by its ID.
    Args:
        transactions: list of transaction dicts, each with an 'id' key.
        target_id: The ID of the transaction to retrieve.
    Returns:
        The matching transaction dict, or None if not found.
    Time Complexity: O(n) where n is the number of transactions.
    Space Complexity: O(1) no additional data structures used.
    """
    for tx in transactions:
        if tx['id'] == target_id:
            return tx
    return None



# Function 4
def sort_by_amount(transactions):
    return sorted(transactions, key=lambda tx: tx['amount'])

# Audited Function 4
def sort_by_amount(transactions):
    """Sorts transactions by their amount in ascending order.
    Args:
        transactions: list of transaction dicts, each with an 'amount' key.
    Returns:
        A new list of transactions sorted by amount.
    Time Complexity: O(1) where n is the number of transactions.
    Space Complexity: O(n) for the new sorted list.
    """
    return sorted(transactions, key=lambda tx: tx['amount'])



# Function 5
def count_by_category(transactions):
    result = {}
    for tx in transactions:
        cat = tx.get('category', 'other')
        if cat not in result:
            result[cat] = 0
        result[cat] += 1
    return result

# Audited Function 5
def count_by_category(transactions):
    # O(n)- Single pass through the transactions dictionary.
    """Counts transactions by their category.
    Args:
        transactions: list of transaction dicts, each with a 'category' key.
    Returns:
        A dictionary with categories as keys and their counts as values.
    Time Complexity: O(n) where n is the number of transactions.
    Space Complexity: O(n) where k is the number of unique categories.
    """
    result = {} #O(n) space atmost n entries in the dictionary
    for tx in transactions:
        cat = tx.get('category', 'other')
        if cat not in result:
            result[cat] = 0
        result[cat] += 1
    return result
# Overall: O(n)time, O(n) space
