"""
demo.py

Demonstration of:
- ManagedDatabase
- managed_query
- timer
- atomic_csv_writer
- multi_resource
"""

from resources import (
    ManagedDatabase,
    managed_query,
    timer,
    atomic_csv_writer,
    multi_resource,
)

import os


DB_PATH = "finance.db"


# ==========================================
# DATABASE SETUP
# ==========================================

with ManagedDatabase(DB_PATH) as conn:

    conn.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            balance REAL NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)


# ==========================================
# INSERT SAMPLE ACCOUNTS
# ==========================================

accounts = [
    (1, "Alice", 1000.0),
    (2, "Bob", 800.0),
    (3, "John", 500.0),
    (4, "Mary", 1200.0),
    (5, "David", 2500.0),
]

with ManagedDatabase(DB_PATH) as conn:

    conn.execute("DELETE FROM accounts")
    conn.execute("DELETE FROM audit_log")

    conn.executemany(
        """
        INSERT INTO accounts
        (id, name, balance)
        VALUES (?, ?, ?)
        """,
        accounts
    )

print("\nInserted sample accounts.\n")


# ==========================================
# DATABASE DECORATOR FACTORY
# ==========================================

db_factory = lambda: ManagedDatabase(DB_PATH)


# ==========================================
# TRANSFER FUNCTION
# ==========================================

@managed_query(db_factory)
def transfer(
    conn,
    from_id,
    to_id,
    amount
):
    """
    Transfer money between accounts.
    """

    sender = conn.execute(
        """
        SELECT * FROM accounts
        WHERE id = ?
        """,
        (from_id,)
    ).fetchone()

    receiver = conn.execute(
        """
        SELECT * FROM accounts
        WHERE id = ?
        """,
        (to_id,)
    ).fetchone()

    if sender["balance"] < amount:
        raise ValueError(
            "Insufficient funds"
        )

    conn.execute(
        """
        UPDATE accounts
        SET balance = balance - ?
        WHERE id = ?
        """,
        (amount, from_id)
    )

    conn.execute(
        """
        UPDATE accounts
        SET balance = balance + ?
        WHERE id = ?
        """,
        (amount, to_id)
    )

    conn.execute(
        """
        INSERT INTO audit_log(event)
        VALUES (?)
        """,
        (
            f"Transfer {amount}"
            f" from {from_id}"
            f" to {to_id}",
        )
    )

    return "Transfer successful"


# ==========================================
# BALANCE HELPER
# ==========================================

@managed_query(db_factory)
def get_balances(conn):

    rows = conn.execute(
        """
        SELECT id, name, balance
        FROM accounts
        ORDER BY id
        """
    )

    return [
        dict(row)
        for row in rows.fetchall()
    ]


# ==========================================
# SUCCESSFUL TRANSFER
# ==========================================

print("=" * 50)
print("SUCCESSFUL TRANSFER")
print("=" * 50)

print(
    transfer(
        1,
        2,
        200
    )
)

for row in get_balances():
    print(row)


# ==========================================
# FAILED TRANSFER
# ==========================================

print("\n" + "=" * 50)
print("FAILED TRANSFER (ROLLBACK)")
print("=" * 50)

try:

    transfer(
        3,
        2,
        100000
    )

except ValueError as e:

    print("Transfer failed:", e)

print("\nBalances after rollback:")

for row in get_balances():
    print(row)


# ==========================================
# TIMER DEMO
# ==========================================

print("\n" + "=" * 50)
print("TIMER DEMO")
print("=" * 50)

with timer(
    "Bulk Insert"
) as result:

    with ManagedDatabase(
        DB_PATH
    ) as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS bulk_data(
                id INTEGER PRIMARY KEY,
                value TEXT
            )
        """)

        conn.execute(
            "DELETE FROM bulk_data"
        )

        conn.executemany(
            """
            INSERT INTO bulk_data(value)
            VALUES (?)
            """,
            [
                (f"row-{i}",)
                for i in range(1000)
            ]
        )

print(
    f"Elapsed: "
    f"{result.elapsed_ms:.2f}ms"
)


# ==========================================
# CSV EXPORT
# ==========================================

print("\n" + "=" * 50)
print("ATOMIC CSV EXPORT")
print("=" * 50)

with ManagedDatabase(DB_PATH) as conn:

    rows = conn.execute(
        """
        SELECT *
        FROM accounts
        """
    ).fetchall()

    rows = [
        dict(row)
        for row in rows
    ]

with atomic_csv_writer(
    "accounts.csv",
    [
        "id",
        "name",
        "balance"
    ]
) as writer:

    writer.writerows(rows)

print(
    "accounts.csv exported!"
)


# ==========================================
# CSV FAILURE DEMO
# ==========================================

print("\n" + "=" * 50)
print("ATOMIC FAILURE TEST")
print("=" * 50)

try:

    with atomic_csv_writer(
        "broken.csv",
        ["id"]
    ) as writer:

        writer.writerow(
            {"id": 1}
        )

        raise RuntimeError(
            "Simulated export failure"
        )

except RuntimeError as e:

    print(
        "Expected failure:",
        e
    )

print(
    "broken.csv exists:",
    os.path.exists(
        "broken.csv"
    )
)


# ==========================================
# MULTI RESOURCE DEMO
# ==========================================

print("\n" + "=" * 50)
print("MULTI RESOURCE DEMO")
print("=" * 50)

with multi_resource(
    ManagedDatabase(DB_PATH),
    ManagedDatabase(DB_PATH),
    timer("Sync Operation")
) as (
    accounts_conn,
    audit_conn,
    timer_result
):

    accounts = accounts_conn.execute(
        """
        SELECT *
        FROM accounts
        """
    ).fetchall()

    audit_conn.execute(
        """
        INSERT INTO audit_log(event)
        VALUES (?)
        """,
        ("sync operation",)
    )

    print(
        f"Loaded "
        f"{len(accounts)} "
        f"accounts"
    )


print("\nDemo Complete!")
