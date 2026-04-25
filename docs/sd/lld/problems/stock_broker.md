# Design Stock Broker

## Terminology Clarification

These two get conflated constantly. Get this right before any design discussion.

|                 | **Stock Exchange**                    | **Stock Broker**                          |
| --------------- | ------------------------------------- | ----------------------------------------- |
| Examples        | NSE, BSE                              | Groww, Zerodha, Upstox                    |
| Role            | Lists stocks, matches buy/sell orders | Intermediary between user and exchange    |
| In this problem | **Publisher** - pushes price updates  | **Subscriber** - receives and stores them |

In this problem we're designing the **broker side**, not the exchange. The exchange is an external system we model just enough to simulate price feeds.

## Problem Statement

Multiple exchanges (NSE, BSE, etc.) continuously push price updates for stock symbols. Design a broker that:

- Receives price updates from any number of exchanges
- Tracks the latest price per symbol
- Stores historical prices per symbol (good-to-have, expected in implementation)
- No REST API needed - CLI + in-memory storage

## Pattern: Observer (Publish-Subscribe)

This is a textbook Observer setup:

- **Subject/Publisher** = `ExchangePublisher` → `IndianStockExchange`
- **Observer/Subscriber** = `Subscriber` → `StockSubscriber`
- **Payload** = `Value(price, currency)`

Why Observer here and not polling? The broker shouldn't be asking exchanges "what's the price now?" on a timer - that's wasteful and adds latency. Exchanges push on every tick; the broker reacts. Observer is the natural fit.
## Class Design

### StockExchange & Subscriber Class Design

Following diagram outlines an Observer Pattern for implementing above question, start with following classes to implement the solution.

**Interfaces**

```
ExchangePublisher (interface)
  subscribe(s: Subscriber)
  unsubscribe(s: Subscriber)
  notify(symbol: str, price: Value)

Subscriber (interface)
  update_stock(symbol: str, price: Value)
```

Both are interfaces (Protocols in Python). `ExchangePublisher` owns the subscriber registry; `Subscriber` is purely reactive - it only receives, never pulls.

![](assets/Pasted%20image%2020251121114652.png)

### Value Object

```
Value { price: int, currency: str }
```

`price` is `int` (paise, cents - never float for money). `currency` makes Value exchange-agnostic: NSE pushes INR, a hypothetical NYSE integration pushes USD.

`Value` is a **value object** - no identity, compared by fields, immutable. 

Use `@dataclass(frozen=True)`.

### Concrete Classes

```
IndianStockExchange (implements ExchangePublisher)
  - conn_url: str
  - api_key: str
  - subscribers: list[Subscriber]

  subscribe(s)    → append to list
  unsubscribe(s)  → remove from list
  notify(sym, v)  → call s.update_stock(sym, v) for each subscriber
  set_price(sym, v) → trigger notify (simulates an incoming tick)
```

`set_price` is your simulation hook - in a real system this would be a WebSocket feed handler. For CLI testing, you call it manually.

```
StockSubscriber (implements Subscriber)
  - symbol: str        ← which symbol this subscriber tracks
  - name: str          ← e.g. "Groww", "Zerodha"
  - price_history: list[Value]   ← append-only; latest is price_history[-1]

  update_stock(sym, v)
    → if sym == self.symbol: append v to price_history
```

**Key design decision: per-symbol or multi-symbol subscriber?** The diagram shows `StockSubscriber` holding a single `symbol`. 

This means one subscriber instance per stock per broker. A broker tracking 500 symbols would have 500 subscriber objects registered on each exchange. That's fine for this problem but worth calling out - a real system would use a single subscriber with a `dict[symbol → list[Value]]`.

### Driver / Main

`DriverClass` creates exchange(s), creates subscribers, subscribes them, then simulates price ticks via `set_price`. The CLI loop can accept commands like:

```
> set INFY 1500 INR       # simulate exchange tick
> get INFY                # show latest price
> history INFY            # show all historical values
> unsub INFY              # unsubscribe from that symbol
```

---

## Data Flow

```
CLI input
    ↓
IndianStockExchange.set_price("INFY", Value(1500, "INR"))
    ↓
for each subscriber in self.subscribers:
    subscriber.update_stock("INFY", Value(1500, "INR"))
    ↓
StockSubscriber (tracking "INFY"):
    price_history.append(Value(1500, "INR"))
```

Multiple exchanges pushing the same symbol → both call `update_stock` on the same subscriber → history interleaves updates from NSE and BSE. If you need to know _which_ exchange sent a price, add `exchange_id` to `Value`.

---

## Historical Price Storage

`price_history: list[Value]` gives you append-only history. Latest price is always `price_history[-1]`. This is O(1) append, O(1) latest lookup.

If you need OHLC (open/high/low/close) later, you'd aggregate over the list - no schema change needed. For now, raw list is correct.

Pandas dataframes actually provide this as a built-in function for OHLC.

**Missing from the original diagram:** `Value` should probably carry a `timestamp` too, or historical data is unorderable if two exchanges push simultaneously. Add it.

---

## Multi-Exchange Consideration

Both `NSE` and `BSE` can list the same stock (INFY, RELIANCE, etc.) and push different prices for the same symbol at the same instant. The subscriber just appends both — that's correct behaviour. The broker's job is to show the **latest received** price, not arbitrate between exchanges.

If you wanted best-price logic (always show the lower ask), that's a separate concern and would live in a `PriceAggregator` layer, not in `StockSubscriber`.

---

## What's Deliberately Missing

- Order placement flow (buy/sell orders back to exchange) - the problem only asks for price tracking
- Authentication / API key validation for exchanges
- Thread safety - `price_history.append` is not atomic under concurrent exchange pushes; fine for single-threaded CLI
- Persistence - in-memory only per requirements

Reference implementation: [https://github.com/singhsanket143/StockBrokerLLD-Problem](https://github.com/singhsanket143/StockBrokerLLD-Problem)

---

## Python Supplement


```python
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol


# --- Value object (immutable, frozen) ---

@dataclass(frozen=True)
class Value:
    price: int          # always int — paise, cents, never float
    currency: str
    timestamp: datetime = field(default_factory=datetime.now)
    # timestamp added: without it, history is unorderable across exchanges


# --- Protocols (structural typing — no forced inheritance) ---

class Subscriber(Protocol):
    def update_stock(self, symbol: str, price: Value) -> None: ...

class ExchangePublisher(Protocol):
    def subscribe(self, s: Subscriber) -> None: ...
    def unsubscribe(self, s: Subscriber) -> None: ...
    def notify(self, symbol: str, price: Value) -> None: ...


# --- Concrete exchange ---

@dataclass
class IndianStockExchange:
    conn_url: str
    api_key: str
    _subscribers: list[Subscriber] = field(default_factory=list)

    def subscribe(self, s: Subscriber) -> None:
        self._subscribers.append(s)

    def unsubscribe(self, s: Subscriber) -> None:
        self._subscribers.remove(s)

    def notify(self, symbol: str, price: Value) -> None:
        """Push to all registered subscribers — they filter by symbol themselves."""
        for s in self._subscribers:
            s.update_stock(symbol, price)

    def set_price(self, symbol: str, price: int, currency: str = "INR") -> None:
        """Simulation hook — replace with WebSocket handler in production."""
        self.notify(symbol, Value(price, currency))


# --- Concrete subscriber ---

@dataclass
class StockSubscriber:
    symbol: str                              # tracks exactly one symbol
    name: str
    price_history: list[Value] = field(default_factory=list)

    def update_stock(self, symbol: str, price: Value) -> None:
        if symbol == self.symbol:
            self.price_history.append(price)

    @property
    def latest(self) -> Value | None:
        """O(1) — history is append-only so latest is always last."""
        return self.price_history[-1] if self.price_history else None


# --- Design decision worth thinking about ---
# Current: one StockSubscriber per symbol. A broker watching 500 symbols
# registers 500 objects on each exchange.
# Alternative: one subscriber with dict[str, list[Value]].
# Trade-off: single object is simpler but symbol filtering moves inside the subscriber.
# For this problem, per-symbol is fine and matches the diagram.


# --- Minimal CLI driver sketch ---

def run_cli(exchanges: list[IndianStockExchange], subscribers: dict[str, StockSubscriber]):
    """Wire up exchanges and enter command loop."""
    print("Commands: set <SYM> <PRICE> | get <SYM> | history <SYM> | quit")
    while True:
        raw = input("> ").strip().split()
        match raw:
            case ["set", sym, price]:
                for ex in exchanges:
                    ex.set_price(sym, int(price))
            case ["get", sym]:
                sub = subscribers.get(sym)
                print(sub.latest if sub else "Not tracked")
            case ["history", sym]:
                sub = subscribers.get(sym)
                if sub:
                    for v in sub.price_history:
                        print(f"  {v.timestamp:%H:%M:%S}  {v.price} {v.currency}")
            case ["quit"]:
                break


# Exercise: add "unsub <SYM>" — unregister the subscriber from all exchanges.
# Where does the exchange reference need to live for this to work?
```

> **Left as exercise:** `unsub` command (subscriber needs a back-reference to its exchanges, or the driver manages this), multi-currency best-price display, and thread-safe history using `collections.deque` with `maxlen` for bounded memory.

---

## Further Reading & Exercises

### Directly Relevant

- _Head First Design Patterns_ - Ch. 2 (Observer Pattern) - the Weather Station example is almost identical in structure to this problem
- _Design Patterns_ (GoF) - Observer (p. 293) - read the "Push vs Pull" model discussion; this design uses push (`notify` carries the value), GoF discusses why that's a trade-off
- Refactoring Guru - [Observer in Python](https://refactoring.guru/design-patterns/observer/python/example)
- Python `typing.Protocol` docs - why `Subscriber` as a Protocol beats an ABC here; any class with `update_stock` qualifies without importing your interface
- _Designing Data-Intensive Applications_ - Ch. 11 (Stream Processing) — what this pattern becomes at scale (Kafka, event streams)

### Exercises

**Easy** - Add `exchange_id: str` to `Value`. Modify `IndianStockExchange` to stamp it on every `Value` it pushes. Now `price_history` tells you which exchange sent each tick.

**Medium** - Right now one `StockSubscriber` tracks one symbol. Refactor to a `BrokerSubscriber` that tracks _all_ symbols using `dict[str, list[Value]]`. What changes in the `update_stock` method? Which design would you use if a broker tracks 10,000 symbols?

**Hard (no single right answer)** - When two exchanges push conflicting prices for the same symbol simultaneously (NSE: 1500, BSE: 1490), what should `latest` return? Option A: last received (current design - timestamp wins). Option B: lower price (best ask). Option C: exchange-specific - NSE always preferred. Where does this logic live - in `StockSubscriber`, a new `PriceAggregator`, or the CLI? Argue one and explain what you'd need to change.

### Related Problems

- **Notification System LLD** - pure Observer; `NotificationService` is the publisher, `EmailHandler`/`SMSHandler`/`PushHandler` are subscribers. Same subscribe/unsubscribe/notify skeleton, different payload.
- **Event Bus / Pub-Sub System LLD** - generalises this: instead of per-exchange publishers, a central `EventBus` dispatches by topic. The `symbol` in this problem is essentially a topic. Direct extension of this design.
- **Ride Sharing - Driver Location Updates** - drivers push location ticks, riders subscribed to that ride receive updates. Same push model; adds the concept of ephemeral subscriptions (subscribe when ride starts, unsubscribe on completion).

### Connection to HLD

The Observer pattern you've designed here is the LLD foundation for several HLD components:

- **Kafka / message queues** - `ExchangePublisher` becomes a Kafka topic; `Subscriber` becomes a consumer group. `notify()` becomes `producer.send()`. The interface contract is identical.
- **WebSocket feeds** - real exchange price feeds are WebSocket streams. `set_price` (your simulation hook) gets replaced by a WebSocket `on_message` handler - zero design change.
- **Fan-out at scale** - if 10,000 broker clients subscribe to INFY, you don't call `update_stock` 10,000 times in a loop. HLD answer: Redis Pub/Sub or SNS fan-out. LLD answer: your `notify()` loop. Same pattern, different execution layer.
- **Event sourcing** - `price_history: list[Value]` is an append-only event log. At HLD scale this becomes a time-series DB (InfluxDB, TimescaleDB). The data model doesn't change.