# Stock Exchange

Problem source: [https://leetcode.com/discuss/post/3636431/phone-pe-machine-coding-stock-exchange-b-x05o/](https://leetcode.com/discuss/post/3636431/phone-pe-machine-coding-stock-exchange-b-x05o/)

## Key Distinction from Stock Broker Problem

In the Stock Broker problem, the broker _subscribes_ to an exchange for price feeds. Here you're **designing the exchange itself** - the thing that receives orders, maintains an order book, and matches buyers with sellers. Completely different responsibility.

| Concept                | Stock Broker LLD        | Stock Exchange LLD           |
| ---------------------- | ----------------------- | ---------------------------- |
| Who are you?           | Broker (Groww, Zerodha) | Exchange (NSE, BSE)          |
| Core challenge         | Observer / price feed   | Order matching + concurrency |
| Primary data structure | `list[Value]` history   | Priority queues per symbol   |
| Pattern used           | Observer                | Strategy (matching algo)     |

## Requirements

**Functional:**

- CRUD on trade orders (create, modify, check status, cancel)
- Buy orders matched with sell orders on **exact price + FIFO** ordering
- Maintain an order book per stock symbol - holds all unexecuted orders
- When a match occurs, a `Trade` record is created

**Non-functional:**

- In-memory storage
- REST API
- Concurrency must be considered - multiple users placing orders simultaneously
- Trade expiry: cancel order if not executed within a specified window



## Class Diagrams

A initial draft could be something like this from a very high level approach

![](assets/Pasted%20image%2020251122232939.png)

Lets refactor this and all the classes & read the question. Trade will be a matched order i.e. when a seller is met with a buyer or vice-versa, we get a trade. Notice Entity classes are already given in the question.

### Refined Design

![](assets/Pasted%20image%2020251122234425.png)

**Core Entities**

```
User       { id, name, phone, email }

Stock      { id, symbol, name, descr, current_price: int, pe_ratio, market_cap: int }

Order      { id, user_id, order_type: OrderType, stock_symbol,
             quantity: int, price: int, order_status: OrderStatus, created_at }

Trade      { id, trade_type, buy_order_id, sell_order_id,
             price: int, qty: int, created_at }
```

**`Trade` is a matched order.** It only exists when a buy meets a sell. It's not an input entity - it's an _output_ of the matching engine. Don't confuse `Order` (intent) with `Trade` (execution).

`price` and `quantity` are always `int`. For price, store in paise/cents.

### Enums

```
OrderType   { BUY, SELL }
OrderStatus { PENDING, ACCEPTED, CANCELLED }
```

- `PENDING` = in order book, waiting for a match. 
- `ACCEPTED` = matched, trade created. 
- `CANCELLED` = expired or user-cancelled. 

There is no `EXECUTED` - that's what `ACCEPTED` means here.

## The Order Book

The order book is the exchange's working memory. One `OrderBook` per stock symbol.

```
OrderBook {
  symbol: str
  buy_queue:  list[Order]    ← sorted: highest price first (max-heap); FIFO within same price
  sell_queue: list[Order]    ← sorted: lowest price first (min-heap); FIFO within same price
}
```

**Why heaps?** You match the best available prices: the highest buy willing to pay, against the lowest sell willing to accept. Heap gives you O(log n) insert and O(1) best-price peek.

**FIFO within same price:** if two buyers both want at ₹1500, the one who placed the order first gets matched first. This is why `created_at` is on `Order` - it's the tiebreaker.

**Exact price match rule (from requirements):** a match only happens when `buy_order.price == sell_order.price`. This is simpler than a real exchange (where any buy price ≥ sell price matches), but it's the stated requirement. Don't generalise it unless asked.

## Service Layer

_Image 3 - OrderBookManagerSVC, OMStrategy / FIFOMatchingStrategy, TradeManagerService, OrderManagerService_

Three services, clear separation of concerns:
### `OrderBookManagerSVC`

```
OrderBookManagerSVC {
  order_book: dict[str, list[Order]]   ← symbol → pending orders (acts as in-memory cache)

  add_order(order: Order)
  get_all_orders_for_symbol(symbol: str) → list[Order]
}
```

This is a thin cache layer over the in-memory order book. It doesn't do matching - it just stores and retrieves pending orders by symbol. Keeping it separate means the matching logic never has to think about storage.

### `OMStrategy` (Order Matching Strategy)

```
OMStrategy (interface/Protocol) {
  get_strategy_name() → str
  match_orders(existing: list[Order], new_order: Order) → list[Trade]
}

FIFOMatchingStrategy implements OMStrategy
```

**Why Strategy here?** The matching algorithm is a hot-swap concern. Today it's FIFO + exact price. Tomorrow it could be pro-rata (split the order across multiple counterparties) or price-time-priority with partial fills. The `OrderManagerService` doesn't need to change - just inject a different `OMStrategy`.

`FIFOMatchingStrategy.match_orders` logic:

1. Filter `existing` to opposite order type (BUY orders if `new_order` is SELL, and vice versa)
2. Filter to exact price match
3. Sort by `created_at` ascending (FIFO)
4. Match greedily: consume from the front until `new_order.quantity` is filled or candidates are exhausted
5. Create `Trade` records for each match; update matched order statuses to `ACCEPTED`

### `OrderManagerService`

```
OrderManagerService {
  order_book_manager: OrderBookManagerSVC
  strategy: OMStrategy

  place_order(dto: OrderRequestDTO) → Order
  cancel_order(order_id: int) → Order
  get_order_status(order_id: int) → OrderStatus
}
```

`place_order` flow:

1. Validate DTO (symbol exists, price > 0, qty > 0)
2. Create `Order` with status `PENDING`, persist to in-memory store
3. Call `order_book_manager.get_all_orders_for_symbol(symbol)`
4. Call `strategy.match_orders(existing, new_order)`
5. If matches found → create Trade(s) via `TradeManagerService`, update statuses
6. If no match → order stays `PENDING` in order book (waits for expiry or cancellation)

### `TradeManagerService`

```
TradeManagerService {
  order_book_manager: OrderBookManagerSVC
  strategy: OMStrategy

  execute_match(buy_order: Order, sell_order: Order) → Trade
}
```

Owns `Trade` creation and the status updates on both matched orders. Keeps trade lifecycle logic out of `OrderManagerService`.

![](assets/Pasted%20image%2020251123002448.png)

**Dependency question worth thinking about:** `OrderManagerService` calls `TradeManagerService` to execute a match, or does `TradeManagerService` call `OrderManagerService`? 

Neither should call the other - they should both be called by a higher-level coordinator (or `OrderManagerService` calls `TradeManagerService` as a downstream, one-way dependency). Circular dependencies between services are a design smell.
### Controllers & DTOs

![](assets/Pasted%20image%2020251123003331.png)

```
OrderController  → handles order CRUD endpoints
UserController   → handles user registration / lookup

OrderRequestDTO {
  stock_symbol: str
  qty: int
  price: int
  order_type: OrderType
  user_id: int
}
```

**Why DTOs?** The API surface and the domain entity are different concerns. `OrderRequestDTO` is what the client sends. `Order` is what the system works with internally. They look similar now but diverge as soon as you add fields like `created_at`, `id`, or `order_status` - which the client should never supply.

DTOs also give you a validation boundary: validate the DTO at the controller level before it ever reaches the service.

### Exception Classes

![](assets/Pasted%20image%2020251123003530.png)

```
Exception
  └── TradeException (base for all domain errors)
        ├── InvalidOrderException   — bad input: negative qty, unknown symbol, etc.
        └── OrderNotFoundException  — cancel/status on an order_id that doesn't exist
```

Controllers catch `TradeException` subclasses and map them to appropriate HTTP status codes (`400` for `InvalidOrderException`, `404` for `OrderNotFoundException`). Nothing else escapes to the HTTP layer.

---

## Concurrency

This is called out in the requirements and is the hardest part. The problem:

Two users simultaneously place a BUY order for the same symbol at the same price against the same SELL order. Without synchronisation, both match against the same sell order → oversell.

**Where to lock:** the critical section is `get_all_orders_for_symbol` → `match_orders` → `execute_match`. This whole sequence must be atomic per symbol.

Options:

- **Per-symbol lock:** `dict[str, Lock]` in `OrderBookManagerSVC`. Lock on the symbol before any match attempt. Different symbols don't contend - high throughput.
- **Global lock:** simpler but serialises all order placement regardless of symbol. Avoid.

In Python: `threading.Lock` per symbol. In a real system: DB row-level locks or a distributed lock (Redis `SET NX`) per symbol.

## Trade Expiry

Order hasn't been matched within N minutes → status = `CANCELLED`, removed from order book.

Implementation options:

- **Background thread / scheduler:** runs every X seconds, scans pending orders, cancels expired ones. Simple. Works for in-memory.
- **Lazy expiry check:** on every `match_orders` call, filter out expired orders before matching. No background thread needed. Risk: expired orders accumulate if no new order triggers a scan for that symbol.

For in-memory + CLI: lazy expiry is fine. For a real system: background job.

---

## What's Deliberately Missing

- Partial fills (order partially matched - e.g., BUY 100 units matched against SELL 60)
- Market orders (execute at best available price, not exact match)
- Order modification endpoint (update price/qty of a pending order)
- Persistence layer

---

## Python Supplement


```python
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Protocol
import threading
import heapq


class OrderType(Enum):
    BUY = auto()
    SELL = auto()

class OrderStatus(Enum):
    PENDING = auto()
    ACCEPTED = auto()
    CANCELLED = auto()


@dataclass
class Order:
    id: int
    user_id: int
    order_type: OrderType
    stock_symbol: str
    quantity: int          # always int
    price: int             # always int (paise/cents)
    order_status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime | None = None   # set on creation if expiry required

    def is_expired(self) -> bool:
        return self.expires_at is not None and datetime.now() > self.expires_at


@dataclass
class Trade:
    id: int
    buy_order_id: int
    sell_order_id: int
    price: int
    qty: int
    created_at: datetime = field(default_factory=datetime.now)


# --- Matching Strategy ---

class OMStrategy(Protocol):
    def get_strategy_name(self) -> str: ...
    def match_orders(self, existing: list[Order], new_order: Order) -> list[tuple[Order, Order]]:
        """Return matched (buy, sell) pairs. Caller creates Trade records."""
        ...

class FIFOMatchingStrategy:
    def get_strategy_name(self) -> str:
        return "FIFO"

    def match_orders(self, existing: list[Order], new_order: Order) -> list[tuple[Order, Order]]:
        """
        Exact price + FIFO.
        Key insight: filter to opposite type FIRST, then price, then sort by created_at.
        """
        opposite = OrderType.SELL if new_order.order_type == OrderType.BUY else OrderType.BUY
        candidates = [
            o for o in existing
            if o.order_type == opposite
            and o.price == new_order.price
            and o.order_status == OrderStatus.PENDING
            and not o.is_expired()
        ]
        candidates.sort(key=lambda o: o.created_at)  # FIFO tiebreak

        matches: list[tuple[Order, Order]] = []
        remaining = new_order.quantity
        for c in candidates:
            if remaining <= 0:
                break
            buy, sell = (new_order, c) if new_order.order_type == OrderType.BUY else (c, new_order)
            matches.append((buy, sell))
            remaining -= c.quantity   # simplified: assumes full fill per counterparty
        return matches


# --- Order Book Manager (per-symbol, thread-safe) ---

class OrderBookManagerSVC:
    def __init__(self) -> None:
        self._book: dict[str, list[Order]] = {}
        self._locks: dict[str, threading.Lock] = {}  # per-symbol lock

    def get_lock(self, symbol: str) -> threading.Lock:
        if symbol not in self._locks:
            self._locks[symbol] = threading.Lock()
        return self._locks[symbol]

    def add_order(self, order: Order) -> None:
        self._book.setdefault(order.stock_symbol, []).append(order)

    def get_pending_orders(self, symbol: str) -> list[Order]:
        return [o for o in self._book.get(symbol, [])
                if o.order_status == OrderStatus.PENDING and not o.is_expired()]


# Exercise: OrderManagerService.place_order() — acquire symbol lock,
# call strategy.match_orders(), create Trade records, update statuses.
# Where does Trade storage live? Argue: TradeManagerService or a separate repo?
```

> **Left as exercise:** `OrderManagerService.place_order` with the lock-acquire-match-release sequence, `TradeManagerService.execute_match`, and the expiry background thread vs lazy expiry decision.

---

## Further Reading & Exercises

### Directly Relevant

- _Designing Data-Intensive Applications_ - Ch. 7 (Transactions) - the lock-per-symbol approach is a practical application of fine-grained locking; read the section on deadlock prevention
- _Clean Architecture_ (Robert Martin) - Ch. 22 (Clean Architecture) - the Controller → Service → Entity layering here is a textbook clean arch slice
- Refactoring Guru - [Strategy Pattern](https://refactoring.guru/design-patterns/strategy) - the `OMStrategy` / `FIFOMatchingStrategy` split is a canonical Strategy example
- Python `threading.Lock` docs - `with lock:` context manager; understand why you need per-symbol locks rather than one global lock
- LeetCode discuss thread linked above - read the original constraints carefully; several common assumptions (e.g. partial fills) are explicitly out of scope

### Exercises

**Easy** - Implement `OrderManagerService.get_order_status(order_id)`. What exception do you raise if the order doesn't exist? Map it to the right HTTP status code in the controller.

**Medium** - Implement trade expiry using lazy expiry: modify `get_pending_orders` to filter out expired orders and flip their status to `CANCELLED` in the same pass. Compare this to a background thread approach - what breaks under high volume with lazy expiry?

**Hard (no single right answer)** - The current design assumes full fills only (a matched order fully consumes the counterparty). Add partial fill support: a BUY for 100 units matches a SELL for 60 → Trade of 60 created, BUY order `quantity` reduced to 40 and stays PENDING. Where does the "remaining quantity" live - mutate `Order.quantity` in place, or add a `filled_quantity` field? Argue both; the answer affects how you reconstruct order history.

### Related Problems

- **BookMyShow LLD** - same core problem: resource contention (seats ≈ order book slots), same lock-before-mutate pattern, same status transition logic. The `ShowSeat` lock maps directly to the per-symbol lock here.
- **Ride Sharing / Uber LLD** - driver-rider matching is structurally identical to order matching: a pool of supply (drivers ≈ sell orders), a pool of demand (riders ≈ buy orders), a matching strategy (nearest driver ≈ FIFO/price). The `OMStrategy` abstraction transfers directly.
- **Parking Lot LLD** - simpler version of the same contention pattern; no matching strategy needed, but the lock-on-resource-before-assign is the same primitive.

### Connection to HLD

- **Order book at scale:** a single `dict[symbol → list[Order]]` in one process doesn't survive restart or scale horizontally. HLD answer: Redis sorted sets (price as score, FIFO via timestamp in the member key) - the heap semantics you need are built in.
- **Matching engine throughput:** real exchanges run the matching engine as a single-threaded event loop (no locks needed - all writes are serialised by design). The per-symbol lock is the LLD approximation of this. At HLD, the answer is a single-threaded Disruptor-pattern queue per symbol.
- **Trade persistence:** `Trade` records created in-memory here become the **event log** at HLD scale - append-only, never updated, used to reconstruct order state. Same design, just durable storage.
- **Concurrency model mismatch:** Python's GIL means `threading.Lock` here is mostly protecting logical atomicity, not CPU parallelism. In a production JVM or Go service, the per-symbol lock is doing real concurrent work. Worth knowing the distinction.
