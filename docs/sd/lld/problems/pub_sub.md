
# CricBuzz Scoreboard Design

## Context

Stadium providers manually enter live match data/commentary → CricBuzz Gateway ingests it → ScoreBoard Service (and hundreds of other internal services) need to consume it.

The design problem is specifically about _how_ the ScoreBoard Service distributes incoming data to its internal display boards.

![](assets/Pasted%20image%2020251117222714.png)

## Iteration 1 – Pull (Polling)

Boards (`RunRateBoard`, `CommentaryBoard`) poll `CricData` on a schedule.

**Data class:**

```
CricData { runs, overs, wickets, innings }
```

![](assets/Pasted%20image%2020251117222747.png)

**Problem:** Wasteful. Boards are hitting the source constantly even when nothing has changed. Doesn't scale as you add boards.

## Iteration 2 – Push (Naive / Direct Coupling)

`CricketData` holds direct references to each board and calls `update()` on all of them.

![](assets/Pasted%20image%2020251117223307.png)

Example Code Snippets

```java
class CricketData {
    private LiveScoreBoard livescoreboard;
    private RunRateBoard runrateboard;
    private CommentaryBoard commentaryBoard;
    
    update() {
        this.livescoreboard.update(...);
        this.runrateboard.update(...);
        ....
    }
}
```

**SOLID violations:**

- **OCP** – adding a new board means modifying `CricketData`. The class is never closed for modification.
- **DIP** – `CricketData` depends on concrete board classes. All boards share the same contract (`update()`); they should be abstracted.

## Iteration 3 – Observer Pattern (Core Design)

Introduce a `Subscriber` interface. `CricketData` holds a list of subscribers and calls `notify()` on every state change. Boards subscribe/unsubscribe at runtime.

`CricketData` (Subject/Publisher)

```
- List<Subscriber> subs
+ notify()          → for each sub: sub.update(ce)
+ subscribe(s)
+ unsubscribe(s)
```

**`<<Subscriber>>` interface**

```
+ update(CricketEvent ce)
```

**Concrete subscribers**

```
CommentaryBoardSub                   RunRateBoardSub
─────────────────                    ───────────────
CommentaryRepo _repo                 (owns its own state)
update(ce) {
  prd.getCE().getCommentary()
  _repo.add(...)
}
```

**`CricketEvent` (payload)**

```
runs, wickets, commentary, live_score, over, ball, ...
```

![](assets/Pasted%20image%2020251117225232.png)

### Why this works

- `CricketData` only knows about the `Subscriber` abstraction → OCP and DIP fixed.
- New board? Implement `Subscriber`, call `subscribe()`. Zero changes to `CricketData`.

![](assets/Pasted%20image%2020251117230329.png)

## Optimization: Selective Subscription (Event Filtering)

`CricketEvent` is a fat payload. `RunRateBoardSub` has no use for commentary fields, and `CommentaryBoardSub` doesn't care about run rate.

**Option:** Subscribers register interest in specific event _types_ rather than all changes.

```
CricketData maintains Map<EventType, List<Subscriber>>
notify(EventType t, CricketEvent ce) → only fans out to subs[t]
```

This keeps boards decoupled from fields they don't own.

## Extension: Multiple Producers

Default design assumes one producer (`CricketData`). Real systems have multiple sources (e.g., ball-tracking feed, official scorecard feed, commentary feed).

**Fix:** Introduce a `Producer` interface. Subscribers maintain a list of producers they're interested in and self-register on construction.


```java
// CommentaryBoardSub
CommentaryRepo _repo;
List<Producer> producers;

constructor(List<Producer> p) {
    this.producers = p;
    for (prod : producers) prod.subscribe(this);
}

update(CricketEvent ce) {
    prd.getCE().getCommentary();
    _repo.add(...);
}
```

`Producer` interface:

```
+ subscribe(Subscriber s)
+ unsubscribe(Subscriber s)
+ getLatestEvent() → CricketEvent
```

This inverts the registration responsibility: the subscriber decides which producers it cares about, not the other way around.

## Missing Requirement Worth Noting

The notes don't cover **thread safety** - in a live match, events arrive concurrently. `subs` list needs protection if subscribers can register/deregister mid-match. In practice: use a `CopyOnWriteArrayList` or lock around `notify()`.

## Python Supplement

```python
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Protocol
from enum import Enum, auto


class EventType(Enum):
    SCORE = auto()
    WICKET = auto()
    COMMENTARY = auto()
    OVER_END = auto()


@dataclass
class CricketEvent:
    event_type: EventType
    runs: int = 0          # int, never float
    wickets: int = 0
    over: int = 0
    ball: int = 0
    commentary: str = ""


class Subscriber(Protocol):
    def update(self, event: CricketEvent) -> None:
        """React to a new cricket event."""
        ...


class Producer(Protocol):
    def subscribe(self, s: Subscriber) -> None: ...
    def unsubscribe(self, s: Subscriber) -> None: ...


@dataclass
class CricketData:
    """Subject. Owns the subscriber list and fan-out logic."""
    _subs: dict[EventType, list[Subscriber]] = field(default_factory=dict)

    def subscribe(self, event_type: EventType, s: Subscriber) -> None:
        self._subs.setdefault(event_type, []).append(s)

    def unsubscribe(self, event_type: EventType, s: Subscriber) -> None:
        self._subs.get(event_type, []).remove(s)

    def notify(self, event: CricketEvent) -> None:
        # Selective fan-out: only subscribers for this event type get called.
        # This is the key design decision vs. notifying everyone always.
        for sub in self._subs.get(event.event_type, []):
            sub.update(event)


class CommentaryBoardSub:
    """Concrete subscriber – only cares about COMMENTARY events."""

    def __init__(self, producers: list[Producer]) -> None:
        self._repo: list[str] = []
        for p in producers:
            p.subscribe(self)   # self-registration; subscriber drives the wiring

    def update(self, event: CricketEvent) -> None:
        if event.commentary:
            self._repo.append(event.commentary)


# Exercise: RunRateBoardSub — implement yourself.
# Tricky part: run rate = total_runs / total_overs, so the board needs
# cumulative state. Decide: does it compute from raw events or receive
# a pre-computed value in CricketEvent?
```

**What's left as an exercise:**

- `RunRateBoardSub` with cumulative state
- Thread-safe `subscribe`/`unsubscribe` (hint: `threading.Lock` around the dict mutation)
- `Producer` concrete implementation that drives `CricketData.notify()`

---

## Further Reading & Exercises

### Directly Relevant

- _Head First Design Patterns_ – Chapter 2 (Observer Pattern). The weather station example maps 1:1 to this problem.
- Python `dataclasses` docs – [https://docs.python.org/3/library/dataclasses.html](https://docs.python.org/3/library/dataclasses.html) (understand `field(default_factory=...)` for mutable defaults)
- `typing.Protocol` docs – [https://docs.python.org/3/library/typing.html#typing.Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol) (structural subtyping; why Protocol beats ABC here)
- _Design Patterns_ (GoF) – Observer pattern, pp. 293–303. Read the "Push vs Pull" trade-off section specifically.
- PEP 544 – [https://peps.python.org/pep-0544/](https://peps.python.org/pep-0544/) (background on Protocols and why they exist)

### Exercises

**Easy** – Add a `LiveScoreBoardSub` that subscribes to `SCORE` and `WICKET` events and maintains a formatted score string like `"IND 142/3 (18.4)"`.

**Medium** – Implement event filtering with a priority queue: high-priority events (WICKET) get dispatched before SCORE updates, even if they arrive out of order. Where does this logic live — in `CricketData.notify()` or outside it?

**Hard (no right answer)** – The `CommentaryBoardSub` currently self-registers with producers in `__init__`. Argue both sides: should the subscriber own registration, or should an external orchestrator wire them up? Consider testability, lifetime management, and what happens when a producer goes offline mid-match. Write a short note defending whichever side you pick.

### Related LLD Problems

- **Stock Ticker / Market Feed** – same Observer pattern, but now you have thousands of subscribers and millisecond-level events. What breaks, and how does an event bus change the design?
- **Notification Service (Email/SMS/Push)** – same fan-out structure; the interesting delta is retry logic and subscriber failure isolation (one dead subscriber shouldn't block others).
- **Pub-Sub / Message Broker (Kafka-lite)** – the natural HLD evolution of this pattern. Topics ≈ `EventType`, consumer groups ≈ subscriber clusters.

### Connection to HLD

This design is the in-process version of a **Pub-Sub broker**. When the ScoreBoard Service itself needs to fan out to hundreds of _external_ services (not just internal boards), you replace `CricketData`'s in-memory list with a Kafka topic. `EventType` becomes a topic partition key. The `Subscriber` interface becomes a consumer group. The design intent is identical; the transport changes.