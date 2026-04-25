# Ecommerce App Design

## Requirements

- Search products from a catalog using composable filter criteria (price range, category, brand, etc.)
- Add products to cart with quantity
- Place an order from cart; support cancellation
- Query current order status (hint: State pattern)

Working constraints: in-memory DB, working code, CLI interaction.

## Two Patterns at Play

This problem is a clean two-pattern problem. Don't conflate them.

| Concern           | Pattern                 | Why                                                           |
| ----------------- | ----------------------- | ------------------------------------------------------------- |
| Product filtering | **Criteria (Strategy)** | Each filter is a strategy; AND/OR are composite strategies    |
| Order lifecycle   | **State**               | Order moves through states with different allowed transitions |
## Part 1 - Criteria / Strategy Pattern

### The Core Problem

_Image - Filter interface with company and price filter implementations; hint points to Chain of Responsibility for AND behaviour._

Chain of Responsibility works for AND-only pipelines (each handler narrows the list). But you also need `OR` - "brand is Apple **or** Samsung". CoR can't express that. So you use the **Criteria pattern**, which is really Strategy + Composite.

Every filter is a `Criteria`. Composite criteria (`AND`, `OR`) themselves implement `Criteria`, so they're arbitrarily nestable:

```
((price > 10 AND price < 1000) OR (brand == 'apple' OR brand == 'samsung'))
```

This is a **Composite pattern** on top of Strategy. `ANDCriteria` and `ORCriteria` hold a list of `Criteria` - each of which may itself be composite.

```
Criteria (interface)
  └── satisfyCriteria(List[Product]) → List[Product]

BrandCriteria(Criteria)       — filters by brand equality
PriceCriteria(Criteria)       — filters by price range (min_price, max_price as int paise/cents)
CategoryCriteria(Criteria)    — filters by category enum

ANDCriteria(Criteria)         — intersection: runs all criteria, returns common products
ORCriteria(Criteria)          — union: runs all criteria, deduplicates by product id
```

![](assets/Pasted%20image%2020251120232719.png)


**ANDCriteria logic:** start with full list, pass through each criterion sequentially. Result is the intersection. Equivalent to `reduce(lambda acc, c: c.satisfy(acc), criteria, products)`.

**ORCriteria logic:** run each criterion on the _original_ full list independently, then union the results. You cannot chain them like AND - each must see the unfiltered list.

This distinction is easy to get wrong in an interview. This is clearly called out here - AND chains, OR fans out.

### Product Entity

```
Product { id: int, name: str, brand: str, category: Category, price: int }
```

`price` is always `int` (paise, cents, etc). `Category` is an `Enum`.

## Part 2 - Cart

Cart is straightforward but has two notable design decisions.

**CartItem vs Product:** cart holds `CartItem(product, quantity)`, not raw products. This lets quantity live on the item rather than on `Product` (which would be wrong - quantity is user-specific).

**Cart ownership:** `Cart` belongs to a `User`. One active cart per user at a time. When an order is placed, the cart is cleared (or marked inactive - your call, but pick one and be consistent).

```
User   { id: int, name: str, cart: Cart }
Cart   { id: int, user_id: int, items: List[CartItem] }
CartItem { product: Product, quantity: int }
```

---

## Part 3 - Order + State Pattern

### Order States

An `Order` moves through a defined lifecycle. Illegal transitions should raise, not silently succeed.

![](assets/Pasted%20image%2020260326192417.png)

`SHIPPED` and `DELIVERED` orders cannot be cancelled - the State pattern enforces this without `if/elif` chains on the `Order` class itself.

### State Pattern Design

Each state is an object that knows which transitions are legal from it. The `Order` holds a reference to its current state and delegates transition calls to it.

```
OrderState (abstract / Protocol)
  ├── confirm(order)   → mutates order.state or raises
  ├── ship(order)      → mutates order.state or raises
  ├── deliver(order)   → mutates order.state or raises
  └── cancel(order)    → mutates order.state or raises

PendingState     — confirm ✓, cancel ✓, ship ✗, deliver ✗
ConfirmedState   — ship ✓, cancel ✓, confirm ✗, deliver ✗
ShippedState     — deliver ✓, cancel ✗
DeliveredState   — all transitions raise (terminal)
CancelledState   — all transitions raise (terminal)
```

`Order` class never has a `match order.status:` block. That logic is fully inside the state objects.

### Order Entity

```
Order {
  id: int
  user_id: int
  items: List[CartItem]   ← snapshot at time of order (not a live reference to cart)
  total: int              ← computed at order creation, stored as int
  state: OrderState
}
```

**Important:** snapshot the cart items at order creation. If cart items were referenced live, a cart modification after ordering would corrupt the order. This is a common gap.

---

## What's deliberately missing

- Payment (out of scope - in-memory, no real transactions)
- Inventory management / stock deduction
- Discount / coupon logic
- Persistence layer (in-memory only per requirements)

---

## Python Supplement


```python
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Protocol
import copy


# --- Domain enums ---

class Category(Enum):
    ELECTRONICS = auto()
    CLOTHING = auto()
    BOOKS = auto()


# --- Product (immutable-ish; price in paise/cents, always int) ---

@dataclass
class Product:
    id: int
    name: str
    brand: str
    category: Category
    price: int   # never float


# --- Criteria pattern ---

class Criteria(Protocol):
    def satisfy(self, products: list[Product]) -> list[Product]: ...

@dataclass
class BrandCriteria:
    brand: str
    def satisfy(self, products: list[Product]) -> list[Product]:
        return [p for p in products if p.brand.lower() == self.brand.lower()]

@dataclass
class PriceCriteria:
    min_price: int
    max_price: int
    def satisfy(self, products: list[Product]) -> list[Product]:
        return [p for p in products if self.min_price <= p.price <= self.max_price]

@dataclass
class ANDCriteria:
    criteria: list[Criteria]
    def satisfy(self, products: list[Product]) -> list[Product]:
        # Each criterion narrows the previous result
        result = products
        for c in self.criteria:
            result = c.satisfy(result)
        return result

@dataclass
class ORCriteria:
    criteria: list[Criteria]
    def satisfy(self, products: list[Product]) -> list[Product]:
        # Each criterion fans out from the ORIGINAL list — not chained
        seen: set[int] = set()
        result: list[Product] = []
        for c in self.criteria:
            for p in c.satisfy(products):
                if p.id not in seen:
                    seen.add(p.id)
                    result.append(p)
        return result


# --- Order State pattern (the trickiest part) ---

class OrderState(Protocol):
    def cancel(self, order: Order) -> None: ...
    def confirm(self, order: Order) -> None: ...
    def ship(self, order: Order) -> None: ...
    def deliver(self, order: Order) -> None: ...

class _IllegalTransition:
    """Mixin: raises for any transition not overridden by the concrete state."""
    def _raise(self, name: str) -> None:
        raise ValueError(f"Cannot {name} from {self.__class__.__name__}")
    def cancel(self, order: Order) -> None: self._raise("cancel")
    def confirm(self, order: Order) -> None: self._raise("confirm")
    def ship(self, order: Order) -> None: self._raise("ship")
    def deliver(self, order: Order) -> None: self._raise("deliver")

class PendingState(_IllegalTransition):
    def confirm(self, order: Order) -> None:
        order.state = ConfirmedState()
    def cancel(self, order: Order) -> None:
        order.state = CancelledState()

class ConfirmedState(_IllegalTransition):
    def ship(self, order: Order) -> None:
        order.state = ShippedState()
    def cancel(self, order: Order) -> None:
        order.state = CancelledState()

class ShippedState(_IllegalTransition):
    def deliver(self, order: Order) -> None:
        order.state = DeliveredState()

class DeliveredState(_IllegalTransition): pass   # terminal
class CancelledState(_IllegalTransition): pass   # terminal


@dataclass
class CartItem:
    product: Product
    quantity: int

@dataclass
class Order:
    id: int
    user_id: int
    items: list[CartItem]  # snapshot — deepcopy from cart at creation
    total: int
    state: OrderState = field(default_factory=PendingState)

    def cancel(self)  -> None: self.state.cancel(self)
    def confirm(self) -> None: self.state.confirm(self)
    def ship(self)    -> None: self.state.ship(self)
    def deliver(self) -> None: self.state.deliver(self)

    @property
    def status(self) -> str:
        return self.state.__class__.__name__.replace("State", "").upper()


# Exercise: Order.items should be a deepcopy of cart items at creation time.
# What breaks if you store a reference instead? Try it.
```

> **Left as exercise:** `Cart` class with `add_item` / `remove_item`, `OrderService.place_order` (deepcopy cart → create Order → clear cart), and the CLI interaction loop.

---

## Further Reading & Exercises

### Directly Relevant

- _Head First Design Patterns_ - Ch. 1 (Strategy), Ch. 9 (Iterator/Composite) — Criteria is a textbook composite-strategy
- _Design Patterns_ (GoF) - Composite (p. 163) and Strategy (p. 315) — read both back to back
- _Head First Design Patterns_ - Ch. 10 (State pattern) — the order lifecycle maps almost exactly to the GumballMachine example
- Refactoring Guru - [Composite](https://refactoring.guru/design-patterns/composite) and [State](https://refactoring.guru/design-patterns/state) — good Python examples
- Python `typing.Protocol` docs - why Protocol beats ABC for Criteria here (structural subtyping, no forced inheritance)

### Exercises

**Easy** - Add a `CategoryCriteria`. Then build: `(brand == 'apple' AND category == ELECTRONICS) OR (price < 50000)`. Write the one-liner that constructs this using `ANDCriteria` + `ORCriteria`.

**Medium** - Implement `Cart` with `add_item(product, qty)` and `remove_item(product_id)`. Then implement `OrderService.place_order(user)`: snapshot the cart, compute total, create `Order` in `PendingState`, clear the cart. What happens if the cart is empty?

**Hard (no single right answer)** - Where does order cancellation eligibility live? Option A: `CancelledState` is only reachable from `Pending` and `Confirmed` - enforced inside state objects (current design). Option B: `Order.cancel()` checks a `cancellable` property before delegating to state. Argue which is more maintainable when you add a "within 30 minutes of shipping" cancellation window. There's no clean answer.

### Related Problems

- **Vending Machine LLD** - purest State pattern problem; states are `Idle`, `HasMoney`, `Dispensing` - same `_IllegalTransition` mixin approach works directly.
- **Ride Sharing (Uber) LLD** - `Trip` has a state machine (REQUESTED → ACCEPTED → IN_PROGRESS → COMPLETED/CANCELLED); Criteria pattern appears again for driver-matching filters.
- **Library Management LLD** - Criteria pattern for book search; no State but adds reservation queue logic that shares the "resource contention + status transitions" DNA with BookMyShow.

### Connection to HLD

At scale these two patterns surface real infrastructure decisions:

**Criteria / filtering:** in-memory filter works for a small catalog. At millions of SKUs you move this to **Elasticsearch** - the `ANDCriteria` / `ORCriteria` tree maps almost 1:1 to ES `bool` query with `must` (AND) and `should` (OR) clauses. Design the Criteria tree now, replace the execution engine later.

**Order State:** in-memory state transitions become **event sourcing** or **saga pattern** at scale. Each `confirm()` / `ship()` / `cancel()` becomes a published event; the state is reconstructed from the event log. The state objects you've designed here become event handlers. The transition rules don't change - only where they execute.