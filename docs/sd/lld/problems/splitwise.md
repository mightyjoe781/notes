# Design SplitWise

## Requirements

**Functional:**

- Create groups; add/remove members
- Add an expense to a group - split equally or by percentage
- View settlements required to settle a group (minimum or simplified transactions)
- View expense history for a group or a specific user

**Solution scope:** End-to-end - REST API layer, service layer, MySQL persistence. Not just class skeletons.

## Data Model (MySQL)

Think in terms of what needs to be queried before designing tables. The two critical queries are:

1. "What does user X owe/is owed across a group?" → `expense_splits` joined to `expenses`
2. "What transactions settle group G?" → derived from summing net balances per user per group


```sql
-- Core tables

CREATE TABLE users (
    id          INT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE groups (
    id          INT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL,
    created_by  INT NOT NULL REFERENCES users(id),
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE group_members (
    group_id    INT REFERENCES groups(id),
    user_id     INT REFERENCES users(id),
    joined_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (group_id, user_id)
);

CREATE TABLE expenses (
    id          INT PRIMARY KEY AUTO_INCREMENT,
    group_id    INT NOT NULL REFERENCES groups(id),
    paid_by     INT NOT NULL REFERENCES users(id),  -- who fronted the money
    amount      INT NOT NULL,                        -- store in paise/cents, never float
    description VARCHAR(255),
    split_type  ENUM('EQUAL', 'PERCENTAGE') NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE expense_splits (
    id          INT PRIMARY KEY AUTO_INCREMENT,
    expense_id  INT NOT NULL REFERENCES expenses(id),
    user_id     INT NOT NULL REFERENCES users(id),
    amount_owed INT NOT NULL,  -- this user's share in paise/cents
    -- For PERCENTAGE splits: store resolved amount, not the percentage itself
    -- Percentage is an input concern, not a storage concern
    UNIQUE (expense_id, user_id)
);
```

**Key schema decisions:**

- **Money is `INT` (paise/cents), never `FLOAT`.** Float arithmetic on currency is a bug waiting to happen. Store ₹10.50 as `1050`.
- **`expense_splits` stores resolved amounts, not percentages.** The percentage is an input detail used to compute the split at write time. Storing raw percentages forces you to re-derive amounts every read, and creates rounding consistency issues.
- **No `settlements` table.** Settlements are derived on-the-fly from `expense_splits`. Persisting them creates a sync problem - every new expense would invalidate cached settlements. Compute, don't store.
- **`group_members` is a join table** - removing a user is a delete on this row. Historical expense splits for that user are preserved (they still owe/are owed money).
## REST API Design

```
# Users
POST   /users                          → create user
GET    /users/{user_id}/expenses       → all expenses for a user

# Groups
POST   /groups                         → create group
POST   /groups/{group_id}/members      → add member
DELETE /groups/{group_id}/members/{user_id}  → remove member

# Expenses
POST   /groups/{group_id}/expenses     → add expense (body: paid_by, amount, split_type, members)
GET    /groups/{group_id}/expenses     → expense history for group

# Settlements
GET    /groups/{group_id}/settlements  → list of transactions to settle the group
```

**POST /groups/{group_id}/expenses - request body:**

```json
{
    "paid_by": 1,
    "amount": 3000,
    "description": "Dinner",
    "split_type": "PERCENTAGE",
    "splits": [
        {"user_id": 1, "percentage": 40},
        {"user_id": 2, "percentage": 35},
        {"user_id": 3, "percentage": 25}
    ]
}
```

For `EQUAL` splits, `splits` is just a list of `user_id`s - the service divides evenly.

**Validation the service layer must do:**

- All `user_id`s in splits must be current group members
- For `PERCENTAGE`: percentages must sum to exactly 100
- For `EQUAL`: divide amount by N; remainder (from integer division) gets added to one split (typically the payer's share, or the first member - be consistent)
- `amount > 0`

---

## Service Layer Class Design

![](assets/Pasted%20image%2020260327004749.png)

---

## Split Strategy (Strategy Pattern - Input Side)

Splits are computed when an expense is created. Two strategies:

![](assets/Pasted%20image%2020260327004106.png)

`EqualSplitStrategy`: `amount // n` per person. Remainder `amount % n` gets distributed one paise at a time to the first `remainder` members. This ensures splits always sum exactly to `amount`.

`PercentageSplitStrategy`: `(percentage * amount) // 100` per person. Same remainder distribution. Validate percentages sum to 100 before computing.

---

## Settlement Strategy (Strategy Pattern - Query Side)

This is the NP-hard problem noted in the original. Two practical approaches:

### Solution 1 - Sequential Settlement (Simple, O(n))

Sort members. Each member settles with the next one in the chain:

- A's net balance is resolved by one transaction with B
- B absorbs A's balance, resolves with C
- Continue until 2 members remain

Produces at most `n-1` transactions. Easy to implement, easy to explain. Not minimal.

### Solution 2 - Greedy Heap Settlement (Fewer Transactions, O(n log n))

```
1. Compute net balance for each user in the group
2. Split into two max-heaps:
     max_creditors: max-heap by amount_owed_to_them  (positive net)
     max_debtors:   max-heap by amount_they_owe      (negative net, stored positive)
3. While both heaps non-empty:
     creditor = max_creditors.pop()  # person owed the most
     debtor   = max_debtors.pop()   # person who owes the most
     settled  = min(creditor.balance, debtor.balance)
     record Transaction(debtor → creditor, settled)
     creditor.balance -= settled
     debtor.balance   -= settled
     if creditor.balance > 0: push back to max_creditors
     if debtor.balance > 0:   push back to max_debtors
```

Each iteration fully settles at least one person (either the creditor or debtor hits zero). At most `2n - 3` transactions for n people. Not provably optimal (that's NP-hard) but good in practice.

**Why two strategies and not just always the greedy one?** The greedy one is more complex to implement, harder to explain, and for small groups (3-4 people) the difference is often 0 transactions. Injecting the strategy lets you switch per group or expose it as a user preference.

![](assets/Pasted%20image%2020260327003820.png)

`Transaction` is a simple value object: `(from_user_id: int, to_user_id: int, amount: int)`.

---

## Net Balance Computation

This is the SQL query the `SettlementService` runs before invoking the strategy:

```sql
-- Net balance per user in a group
-- Positive = net creditor, Negative = net debtor
SELECT
    u.id,
    u.name,
    SUM(
        CASE WHEN e.paid_by = u.id THEN es.amount_owed ELSE 0 END  -- what others owe you
        -
        CASE WHEN es.user_id = u.id AND e.paid_by != u.id THEN es.amount_owed ELSE 0 END  -- what you owe
    ) AS net_balance
FROM users u
JOIN group_members gm ON gm.user_id = u.id
JOIN expense_splits es ON es.user_id = u.id
JOIN expenses e ON e.id = es.expense_id AND e.group_id = gm.group_id
WHERE gm.group_id = ?
GROUP BY u.id;
```

The strategy receives this `dict[user_id → net_balance_int]` and produces `list[Transaction]`. The service layer is the only thing that knows about SQL; the strategy is pure Python.

---

## What's Not Covered (Intentionally)

- **Authentication / authorisation** - assume a `user_id` header on all requests. In production, JWT + middleware.
- **Partial settlements** - user pays part of what they owe. Requires a `payments` table and adjusting net balance computation. Non-trivial extension.
- **Multi-currency** - store `currency` on `expenses`. Net balance computation becomes per-currency or requires FX conversion. Out of scope here.
- **Notifications** - when an expense is added, notify affected members. Event-driven; publish to a queue after `ExpenseService.add_expense` writes to DB.

---

## Python Supplement


```python
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Protocol
import heapq


class SplitType(Enum):
    EQUAL = auto()
    PERCENTAGE = auto()


@dataclass
class SplitInput:
    user_id: int
    percentage: int = 0  # only used for PERCENTAGE splits


@dataclass(frozen=True)
class SplitResult:
    user_id: int
    amount_owed: int  # resolved amount in paise, always int


@dataclass(frozen=True)
class Transaction:
    from_user_id: int
    to_user_id: int
    amount: int  # paise


# ── Split Strategies ──────────────────────────────────────────────────────────

class SplitStrategy(Protocol):
    def compute(self, amount: int, members: list[SplitInput]) -> list[SplitResult]: ...


class EqualSplitStrategy:
    def compute(self, amount: int, members: list[SplitInput]) -> list[SplitResult]:
        n = len(members)
        base, remainder = divmod(amount, n)
        # Distribute remainder one paise at a time - splits always sum to amount
        return [
            SplitResult(m.user_id, base + (1 if i < remainder else 0))
            for i, m in enumerate(members)
        ]


class PercentageSplitStrategy:
    def compute(self, amount: int, members: list[SplitInput]) -> list[SplitResult]:
        if sum(m.percentage for m in members) != 100:
            raise ValueError("Percentages must sum to 100.")
        results = [(amount * m.percentage) // 100 for m in members]
        remainder = amount - sum(results)
        return [
            SplitResult(m.user_id, results[i] + (1 if i < remainder else 0))
            for i, m in enumerate(members)
        ]


# ── Settlement Strategies ─────────────────────────────────────────────────────

class SettlementStrategy(Protocol):
    def settle(self, balances: dict[int, int]) -> list[Transaction]: ...


class GreedySettlementStrategy:
    def settle(self, balances: dict[int, int]) -> list[Transaction]:
        # Trickiest part: two max-heaps (negate for Python's min-heap)
        creditors: list[tuple[int, int]] = []  # (-balance, user_id)
        debtors: list[tuple[int, int]] = []

        for uid, bal in balances.items():
            if bal > 0:
                heapq.heappush(creditors, (-bal, uid))
            elif bal < 0:
                heapq.heappush(debtors, (bal, uid))  # already negative

        transactions: list[Transaction] = []
        while creditors and debtors:
            c_bal, c_uid = heapq.heappop(creditors)
            d_bal, d_uid = heapq.heappop(debtors)
            c_bal, d_bal = -c_bal, -d_bal  # make positive for arithmetic

            settled = min(c_bal, d_bal)
            transactions.append(Transaction(d_uid, c_uid, settled))

            if (c_bal - settled) > 0:
                heapq.heappush(creditors, (-(c_bal - settled), c_uid))
            if (d_bal - settled) > 0:
                heapq.heappush(debtors, (-(d_bal - settled), d_uid))

        return transactions


# Left as exercise:
# - SequentialSettlementStrategy (simpler, O(n))
# - ExpenseService._compute_splits dispatcher (match split_type: ...)
# - SettlementService.get_settlements: run SQL → call strategy → return Transactions
# - Remainder handling edge case: what if amount is not divisible by n and n > amount?
```

**Trickiest design decision - where does remainder paise go?**  
Integer division of 100 paise among 3 people gives 33 + 33 + 33 = 99. The missing 1 paise must be assigned somewhere deterministically. Giving it to `members[0]` (the payer) is common. Whatever you choose, it must be consistent - inconsistency causes net balances to not sum to zero, which breaks settlement.

---

## Further Reads & Exercises

### Directly Relevant

1. **Refactoring.Guru - Strategy Pattern** - [https://refactoring.guru/design-patterns/strategy](https://refactoring.guru/design-patterns/strategy) - the SplitStrategy and SettlementStrategy hierarchies are textbook uses.
2. **"Designing Data-Intensive Applications" - Kleppmann, Ch. 1** - fundamentals of why you derive settlements rather than storing them (derived data vs source-of-truth).
3. **Martin Fowler - Money Pattern** - [https://martinfowler.com/eaaCatalog/money.html](https://martinfowler.com/eaaCatalog/money.html) - canonical treatment of why currency is never a float.
4. **Splitwise engineering blog** - [https://blog.splitwise.com/2012/09/14/debts-across-a-group/](https://blog.splitwise.com/2012/09/14/debts-across-a-group/) - their actual writeup on the debt simplification algorithm.
5. **Python `heapq` docs** - [https://docs.python.org/3/library/heapq.html](https://docs.python.org/3/library/heapq.html) - `heapq` is a min-heap; negate values for max-heap behaviour (used in `GreedySettlementStrategy`).

### Exercises

**Easy** - Implement `SequentialSettlementStrategy`. Sort users by net balance, iterate, chain settlements. Verify it produces exactly `n-1` transactions.

**Medium** - Add a `payments` table to the schema to support partial settlements (user pays part of what they owe outside the app). How does `_compute_net_balances` change? What's the new SQL query?

**Hard (no right answer)** - Should `SettlementService` cache the settlement results? Arguments for: expensive to recompute for large groups, called frequently on read. Arguments against: any new expense invalidates the cache, stale settlements are worse than slow ones. What's your invalidation strategy, and does it change if you use Redis vs a `settlements` table in MySQL? Argue both sides.

### Related LLD Problems

|Problem|What transfers|
|---|---|
|**Bill Splitting / Expense Tracker (simpler)**|Same `expense_splits` data model; drop the settlement strategy entirely if you only need per-person totals.|
|**Payment Gateway / Wallet**|The `Transaction` value object and integer money arithmetic carry over directly. Settlement becomes a ledger problem.|
|**Task Assignment / Scheduling**|The greedy heap pattern (match the most-loaded to the least-loaded) is identical in structure to the greedy settlement algorithm - different domain, same algorithm.|

### Connection to HLD Problems

Two HLD concepts surface directly here:

**Derived data vs source of truth** - The decision not to store settlements is a specific instance of a general HLD principle: derived data (settlements, totals, rankings) should be computed from the source of truth (expense_splits), not stored independently. In HLD, this maps to the read model in CQRS, or a materialised view. When reads get expensive, you materialise - but you accept eventual consistency and a cache invalidation strategy. The "Hard" exercise above is exactly this tradeoff.

**Ledger / double-entry bookkeeping** - At scale, Splitwise's data model converges toward a ledger: every expense creates debit/credit entries, and balance = sum of all entries. This is how every financial system (Stripe, banks) works internally. The `expense_splits` table here is a simplified single-entry ledger. Understanding this makes the transition to HLD financial systems straightforward.