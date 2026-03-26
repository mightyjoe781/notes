# Design BookMyShow

## Core Problem

Any booking system is fundamentally a **resource contention** problem: multiple users racing for the same finite seats in the same show. The two standard solutions:

|Strategy|Mechanism|When to use|
|---|---|---|
|**Pessimistic lock**|Acquire DB row lock before the transaction starts|High contention (popular shows)|
|**Optimistic lock**|Version column on the row; fail on mismatch at commit|Low-to-medium contention
BookMyShow warrants **pessimistic locking** on `ShowSeat` rows - a Friday night premiere will have dozens of concurrent users hitting the same seats. A failed `SELECT FOR UPDATE` is cheaper than a rollback storm from optimistic collisions.

> Reference for both approaches: the RDBMS System Design note linked in the original.

More Details here : [RDBS System Design](../../hld/advanced/relational_database.md)

## Requirements

- REST API with proper DB integration
- Fully working booking flow (seat selection → lock → payment → confirm/release)
- Seats locked during payment window; released on timeout or failure

## Class Design

### Movie Class

![](assets/Pasted%20image%2020251120001835.png)

`Movie` holds a list of supported languages. 

Simple composition - a movie doesn't _own_ a language (languages exist independently), so this is an association, not aggregation.
### Theatre → Audi → Seat

Theatre hierarchy and ShowSeat join table.

`Seat` represents the **physical** chair - it doesn't change between shows. `type` covers things like RECLINER, NORMAL, VIP.

Key decision: **`Seat.status` alone is not enough.** 

A seat being "available" in the physical audi doesn't mean it's free for _this_ show. That's why we need `ShowSeat`.

![](assets/Pasted%20image%2020251120001942.png)

`ShowSeat` is the per-show snapshot of every seat's availability. When a user tries to book, you lock `ShowSeat` rows - not `Seat` rows. `Seat` is immutable physical data.

![](assets/Pasted%20image%2020251120002338.png)

Audi grid showing blocked (pink) vs available (green) seats. This is exactly what `ShowSeat.status` models at runtime.

Status Transition : 

```
AVAILABLE → LOCKED (user selects seat)
LOCKED    → BOOKED  (payment succeeds)
LOCKED    → AVAILABLE (payment timeout / failure)
```
### Ticket Entity

![](assets/Pasted%20image%2020251120003218.png)

A `Ticket` is the **receipt** - it's created only after a booking is confirmed. Don't create a `Ticket` at the lock step. `show_seat` is included so you can always trace back to the exact per-show seat record.

## Booking Flow

1. User selects seats for a show
2. SELECT FOR UPDATE on ShowSeat rows (pessimistic lock)
3. Validate all are AVAILABLE → set status = LOCKED
4. Initiate payment (timeout window, e.g. 10 min)
5. a. Payment success → status = BOOKED, create Ticket
6. b. Payment fail / timeout → status = AVAILABLE, release lock

Step 2–3 must be inside a single DB transaction.

## What's deliberately missing here

- Payment gateway integration (out of scope for LLD)
- Notification service (email/SMS on booking)
- Waitlist / queue handling for sold-out shows
- Seat recommendation logic

Reference implementation: [https://github.com/singhsanket143/LLD-BookMyShow](https://github.com/singhsanket143/LLD-BookMyShow)

---
## Python Supplement


```python
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime


# --- Enums ---

class SeatType(Enum):
    NORMAL = auto()
    RECLINER = auto()
    VIP = auto()

class ShowSeatStatus(Enum):
    AVAILABLE = auto()
    LOCKED = auto()      # held during payment window
    BOOKED = auto()

class TicketStatus(Enum):
    CONFIRMED = auto()
    CANCELLED = auto()


# --- Physical layout (immutable after setup) ---

@dataclass
class Seat:
    id: int
    type: SeatType
    # no status here — physical seats don't have per-show availability

@dataclass
class Audi:
    id: int
    name: str
    seats: list[Seat] = field(default_factory=list)

@dataclass
class Theatre:
    id: int
    name: str
    audis: list[Audi] = field(default_factory=list)


# --- Per-show state ---

@dataclass
class Show:
    id: int
    movie_id: int
    audi_id: int
    start_time: datetime
    end_time: datetime

@dataclass
class ShowSeat:
    id: int
    show_id: int
    seat_id: int
    status: ShowSeatStatus = ShowSeatStatus.AVAILABLE
    # In a real DB this row gets SELECT FOR UPDATE in the booking txn


# --- Booking service (trickiest design decision) ---

class BookingService:
    """
    Where does the lock logic live? Here, not on ShowSeat itself.
    ShowSeat is a data object; the service owns the transaction boundary.
    """

    def lock_seats(self, show_seat_ids: list[int], user_id: int) -> list[ShowSeat]:
        """Acquire pessimistic lock; raise if any seat is not AVAILABLE."""
        # Pseudocode — real impl wraps this in a DB transaction
        seats = self._fetch_for_update(show_seat_ids)   # SELECT FOR UPDATE
        unavailable = [s for s in seats if s.status != ShowSeatStatus.AVAILABLE]
        if unavailable:
            raise ValueError(f"Seats already taken: {[s.id for s in unavailable]}")
        for seat in seats:
            seat.status = ShowSeatStatus.LOCKED
        return seats

    def confirm_booking(self, show_seat_ids: list[int], user_id: int) -> Ticket:
        """Call after payment succeeds."""
        ...

    def release_seats(self, show_seat_ids: list[int]) -> None:
        """Call on payment timeout or failure."""
        ...

    def _fetch_for_update(self, ids: list[int]) -> list[ShowSeat]:
        ...  # DB layer: SELECT * FROM show_seat WHERE id IN (...) FOR UPDATE


@dataclass
class Ticket:
    id: int
    show_seat_ids: list[int]
    user_id: int
    show_id: int
    status: TicketStatus = TicketStatus.CONFIRMED


# Exercise: where does the 10-minute lock timeout live?
# Option A: a background job scans LOCKED rows past deadline → release
# Option B: application-level TTL checked at confirm time
# Argue both sides.
```

> **Left as exercise:** payment gateway integration, the timeout/release mechanism, and `ShowSeat` initialisation when a new `Show` is created (bulk-insert one row per seat in the audi).

---

## Further Reading & Exercises

### Resources

- _Designing Data-Intensive Applications_ - Ch. 7 (Transactions, isolation levels, SELECT FOR UPDATE)
- _System Design Interview Vol. 2_ - Ticketmaster chapter (same contention problem, larger scale)
- PostgreSQL docs - [Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html) (row-level locks, `FOR UPDATE` semantics)
- Martin Fowler - [Pessimistic Offline Lock](https://martinfowler.com/eaaCatalog/pessimisticOfflineLock.html)
- SQLAlchemy docs - [with_for_update()](https://docs.sqlalchemy.org/en/20/orm/query.html#sqlalchemy.orm.Query.with_for_update) (how to do this in Python ORM)

### Exercises

**Easy** - Implement `BookingService.release_seats()`. What HTTP status code should the REST endpoint return when seats are already locked by another user?

**Medium** - Implement the `Show` creation flow: when a new `Show` is inserted, `ShowSeat` rows must be auto-created for every seat in the audi. Where does this logic live — service layer, DB trigger, or event? Argue one.

**Hard (no single right answer)** - The lock timeout: should it be a background cron job that scans the DB for expired `LOCKED` rows, or application-level TTL enforced at confirm-time? Write out the failure modes of each. Which breaks worse under load?

### Related Problems

- **Parking Lot LLD** - same pattern: a finite physical resource (`ParkingSpot` ≈ `Seat`), per-session state (`ParkingTicket` ≈ `ShowSeat`), and status transitions. Almost a 1:1 mapping.
- **Hotel Booking / Airbnb LLD** - same contention on `RoomAvailability` rows; adds date-range overlap queries on top of the lock logic.
- **Flash Sale / Inventory LLD** - same pessimistic-vs-optimistic decision, but at much higher throughput; introduces Redis-based locking as an alternative to DB row locks.

### Connection to HLD

At HLD scale this problem becomes: how do you maintain seat availability across multiple app servers without every request hitting the primary DB? Common additions:

- **Redis** for the lock layer (`SET NX EX` for seat IDs) - offloads `SELECT FOR UPDATE` from DB
- **Message queue** (Kafka/SQS) for async payment confirmation → `ShowSeat` status update
- **Read replicas** for the seat availability query (read-heavy); writes (locks/confirms) still go to primary
- **Sticky sessions or consistent hashing** if you shard show data - all requests for a given `show_id` should ideally hit the same DB shard to localise lock contention