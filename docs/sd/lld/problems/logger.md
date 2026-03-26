# Logging Framework

Every programming language has some kind of logging framework. In an ideal scenario, you might wonder: _why do we even need a logger at all?_

Can’t you just run `print` or `cout` statements and direct the output to stdout or a file?

Of course you **can** do that, but a logging framework tries to **standardize and unify** how logs are produced and managed. For example, imagine you’ve imported a library that makes network calls. You don’t want to see every single detail that the library prints - that would be a disaster. The library might give you a switch to toggle some of that output, but it would still be very difficult to control the _level_ and _verbosity_ of the logs in a consistent way.

A logging framework solves this by introducing concepts like **log levels**, **appenders**, and **formatters**. These let you control verbosity, decide where logs go, and structure them for log-analysis tools - all without scattering arbitrary print statements throughout your code.

The following LLD problem involves designing a basic replica of these features.

## Requirements

- Log levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `FATAL`
- Each log message carries: level, content, timestamp
- Multiple output destinations (console, file, database) - configurable
- Configurable minimum log level: messages below the threshold are silently dropped
- Thread-safe: concurrent logging from multiple threads must not interleave or corrupt output
- Extensible: new levels and appenders without modifying existing code

## Design: Three-Layer Architecture

Every logging framework is built on the same three abstractions:

The `Logger` decides _whether_ to log (level filter). 

The `LogAppender` decides _where_ to write. The `LogFormatter` decides _how_ to render the message. These three concerns are always separate.

Good Video explaining Logging Module in `python` : https://www.youtube.com/watch?v=9L77QExPmI0
## Layer 1 - Data Models

![](assets/Pasted%20image%2020251212220433.png)

**`LogLevel` Enum** - ordered integers matter here. The ordering is what enables level filtering: "only log messages at WARN or above." `DEBUG=0` is least severe, `FATAL=4` is most.

```
LogLevel: DEBUG=0, INFO=1, WARN=2, ERROR=3, FATAL=4
```

**`LogMessage`** - plain value object. Created once, never mutated. Holds:

- `level: LogLevel`
- `content: str`
- `timestamp: datetime` ← `timestamp: obj` in the diagram means `datetime.datetime`

`LogMessage` is constructed by the `Logger` when a log call is made, not by the caller. The caller just passes a string.

## Layer 2 - Appenders and Formatters

![](assets/Pasted%20image%2020251212221244.png)
### `LogFormatter` (Interface)

```
<<LogFormatter>>
+ format(msg: LogMessage) → str
```

Concrete implementation: `SimpleTextFormatter`

```python
def format(msg):
    return f"{msg.timestamp} | {msg.level.name} | {msg.content}"
```

`LogFormatter` is an interface so you can swap in a `JSONFormatter` for log-analysis tools (Splunk, ELK) without touching the appender.

### `LogAppender` (Interface/Abstract)


`LogAppender` _owns_ a `LogFormatter`. The formatter is an implementation detail of the appender - the caller (Logger) just calls `append(msg)` and doesn't know or care how it's formatted.

**Concrete implementations:**

|Appender|`append()` does|`close()` does|
|---|---|---|
|`ConsoleAppender`|`print(formatter.format(msg))`|`pass`|
|`FileAppender`|`file.write(formatter.format(msg) + "\n")`|`file.close()`|
|`DatabaseAppender`|`db.execute(INSERT ...)`|`connection.close()`|

`close()` exists because some appenders hold external resources (file handles, DB connections) that must be released. The interface forces every appender to declare this explicitly, even if it's a no-op.

**Thread safety lives in the appender, not in the Logger.** `ConsoleAppender` is trivially safe. `FileAppender` needs a `threading.Lock` around the write. `DatabaseAppender` can use connection pooling. Each appender manages its own concurrency - the Logger doesn't need to know.

## Layer 3 = The Logger

```
<<Logger>>
──────────────────────────────────────────────
name: str
parent: Logger | None
level: LogLevel
appenders: list[LogAppender]
additivity: bool

log(level, msg_str) → None
debug(msg_str)  → log(DEBUG, msg_str)
info(msg_str)   → log(INFO,  msg_str)
warn(msg_str)   → log(WARN,  msg_str)
error(msg_str)  → log(ERROR, msg_str)
fatal(msg_str)  → log(FATAL, msg_str)
```

### Logger Hierarchy and `parent`

This is the most important concept and the most under-explained.

Every logger has a `name` (e.g., `"myapp"`, `"myapp.db"`, `"myapp.network"`). The root logger is the ancestor of all others. Naming convention is dotted hierarchy — `"myapp.db"` is a child of `"myapp"`, which is a child of `root`.

Why? Because you want fine-grained control:

- Root logger: level `WARN` → only warnings and above globally
- `"myapp.db"` logger: level `DEBUG` → see every DB query during debugging
- `"myapp.network"` logger: level `ERROR` → suppress noisy network info logs

Without hierarchy, you'd need to reconfigure every logger individually every time.

### Level Filtering

```python
def log(self, level: LogLevel, msg_str: str) -> None:
    if level.value < self.level.value:
        return  # drop silently — below threshold
    msg = LogMessage(level=level, content=msg_str, timestamp=datetime.now())
    for appender in self.appenders:
        appender.append(msg)
    if self.additivity and self.parent:
        self.parent.log(level, msg_str)  # propagate up the hierarchy
```

### `additivity` — The Key Field

If `additivity=True` (the default), a log event propagates up to the parent logger after being handled. This means if `"myapp.db"` has a `FileAppender` and root has a `ConsoleAppender`, a DB log goes to both file _and_ console.

If `additivity=False`, propagation stops at this logger. Set this when you have a child logger that should be completely isolated from the root (e.g., an audit logger that must only write to a secure file, never to console).

The classic bug: forgetting `additivity=False` on a noisy child logger and flooding root with debug output.
### Logger as Singleton (per name)

Loggers must be singletons keyed by name. If two classes both call `Logger.get_logger("myapp.db")`, they must get the same instance — otherwise configuration on one doesn't affect the other. Use a class-level registry:

```python
_registry: dict[str, Logger] = {}

@classmethod
def get_logger(cls, name: str) -> Logger:
    if name not in cls._registry:
        cls._registry[name] = cls._create(name)
    return cls._registry[name]
```

This is a **Multiton** - same idea as Singleton but keyed. Thread-safe registry access needs a lock too.

![](assets/Pasted%20image%2020251212221542.png)

## Thread Safety Summary

Thread safety is a requirement. Where exactly does it live?

|Concern|Who handles it|How|
|---|---|---|
|Logger registry access|`Logger.get_logger`|`threading.Lock` on `_registry` write|
|File writes|`FileAppender.append`|`threading.Lock` per file handle|
|DB writes|`DatabaseAppender.append`|connection pool handles it|
|Console writes|`ConsoleAppender.append`|`print()` is GIL-safe in CPython; explicit lock for safety|

Do not put a single global lock on the `Logger.log()` method — that serialises all logging across all threads. Lock at the appender level for better throughput.

---

## What's Not Covered (Intentionally)

- **Configuration from file** (e.g., `logging.ini`, `logging.yaml`) - deserialise config and call `Logger.get_logger(...).set_level(...)`. Straightforward once the class hierarchy is solid.
- **Log rotation** for `FileAppender` - when file hits a size limit, rename it and open a new one. `logging.handlers.RotatingFileHandler` in Python stdlib does this.
- **Async logging** - buffered queue between `Logger` and `AppenderWorker`. Useful when DB writes are slow; logs go to a queue and a background thread drains it.

---

## Python Supplement

```python
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum
from typing import Protocol
import threading


class LogLevel(IntEnum):
    # IntEnum so comparisons (level >= threshold) work naturally
    DEBUG = 0
    INFO  = 1
    WARN  = 2
    ERROR = 3
    FATAL = 4


@dataclass(frozen=True)
class LogMessage:
    level: LogLevel
    content: str
    timestamp: datetime = field(default_factory=datetime.now)


# ── Formatter ─────────────────────────────────────────────────────────────────

class LogFormatter(Protocol):
    def format(self, msg: LogMessage) -> str: ...


class SimpleTextFormatter:
    def format(self, msg: LogMessage) -> str:
        return f"{msg.timestamp.isoformat()} | {msg.level.name:<5} | {msg.content}"


# ── Appenders ─────────────────────────────────────────────────────────────────

class LogAppender(Protocol):
    def append(self, msg: LogMessage) -> None: ...
    def close(self) -> None: ...


class ConsoleAppender:
    def __init__(self, formatter: LogFormatter = SimpleTextFormatter()) -> None:
        self._formatter = formatter
        self._lock = threading.Lock()

    def append(self, msg: LogMessage) -> None:
        with self._lock:  # GIL helps but explicit lock is correct practice
            print(self._formatter.format(msg))

    def close(self) -> None:
        pass


class FileAppender:
    def __init__(self, filepath: str, formatter: LogFormatter = SimpleTextFormatter()) -> None:
        self._formatter = formatter
        self._file = open(filepath, "a", encoding="utf-8")
        self._lock = threading.Lock()  # lock is per-file-handle

    def append(self, msg: LogMessage) -> None:
        with self._lock:
            self._file.write(self._formatter.format(msg) + "\n")
            self._file.flush()  # don't buffer — crash safety

    def close(self) -> None:
        with self._lock:
            self._file.close()


# ── Logger ────────────────────────────────────────────────────────────────────

class Logger:
    _registry: dict[str, Logger] = {}
    _registry_lock = threading.Lock()

    def __init__(
        self,
        name: str,
        level: LogLevel = LogLevel.WARN,
        appenders: list[LogAppender] | None = None,
        parent: Logger | None = None,
        additivity: bool = True,
    ) -> None:
        self.name = name
        self.level = level
        self.appenders: list[LogAppender] = appenders or []
        self.parent = parent
        self.additivity = additivity

    @classmethod
    def get_logger(cls, name: str) -> Logger:
        """Multiton — same name always returns same instance."""
        with cls._registry_lock:
            if name not in cls._registry:
                cls._registry[name] = Logger(name=name)
            return cls._registry[name]

    def log(self, level: LogLevel, content: str) -> None:
        if level < self.level:
            return  # IntEnum comparison — drop if below threshold
        msg = LogMessage(level=level, content=content)
        for appender in self.appenders:
            appender.append(msg)
        if self.additivity and self.parent is not None:
            self.parent.log(level, content)  # propagate up

    # Convenience methods — just sugar over log()
    def debug(self, msg: str) -> None: self.log(LogLevel.DEBUG, msg)
    def info(self,  msg: str) -> None: self.log(LogLevel.INFO,  msg)
    def warn(self,  msg: str) -> None: self.log(LogLevel.WARN,  msg)
    def error(self, msg: str) -> None: self.log(LogLevel.ERROR, msg)
    def fatal(self, msg: str) -> None: self.log(LogLevel.FATAL, msg)


# Trickiest design decision: additivity + propagation
# root gets ALL logs from children unless child sets additivity=False
root = Logger.get_logger("root")
root.level = LogLevel.WARN
root.appenders = [ConsoleAppender()]

db_logger = Logger.get_logger("myapp.db")
db_logger.level = LogLevel.DEBUG
db_logger.appenders = [FileAppender("db.log")]
db_logger.parent = root
db_logger.additivity = True   # DEBUG+ goes to db.log AND propagates to root
                               # root drops it (level=WARN) — no double print
                               # set False to fully isolate from root

# Left as exercise: LoggerFactory with auto parent resolution from name,
# config from dict/yaml, async buffered appender with queue + worker thread
```

**Why `IntEnum` and not `Enum(auto())`?**  
`LogLevel` needs `<` comparison (`level < self.level`) to be natural. `IntEnum` gives this for free. With plain `Enum`, you'd compare `.value` explicitly everywhere - more brittle.

**Why lock per appender, not per logger?**  
A single lock on `Logger.log()` serialises all threads for all destinations. Two threads writing to different files would block each other unnecessarily. Appender-level locks let unrelated appenders run concurrently.

---

## Further Reads & Exercises

### Directly Relevant

1. **Python `logging` module docs** - [https://docs.python.org/3/library/logging.html](https://docs.python.org/3/library/logging.html) - the stdlib is a direct implementation of these exact concepts; read `Logger`, `Handler`, `Formatter` class docs.
2. **Python `logging` HOWTO** - [https://docs.python.org/3/howto/logging.html](https://docs.python.org/3/howto/logging.html) - covers hierarchy, propagation, and `additivity` (called `propagate` in stdlib) with examples.
3. **Video: Python logging module deep dive** - [https://www.youtube.com/watch?v=9L77QExPmI0](https://www.youtube.com/watch?v=9L77QExPmI0) - from your notes; covers hierarchy and handler setup well.
4. **"Effective Java" 3rd ed. - Item 3 (Singleton)** - Multiton is the same idea; good grounding on why registry-based singletons are safer than module-level globals.
5. **Log4j architecture docs** - [https://logging.apache.org/log4j/2.x/manual/architecture.html](https://logging.apache.org/log4j/2.x/manual/architecture.html) — the original source for Logger/Appender/Formatter as a pattern; still the clearest explanation of additivity.

### Exercises

**Easy** - Implement `JSONFormatter`. Output: `{"timestamp": "...", "level": "WARN", "message": "..."}`. Plug it into `FileAppender`. What changes in the calling code? (Nothing - that's the point.)

**Medium** - Implement an async `BufferedAppender` that wraps any `LogAppender`. It accepts messages into a `queue.Queue`, and a background daemon thread drains the queue and calls the wrapped appender's `append()`. How do you handle flush-on-shutdown?

**Hard (no right answer)** - Where should the minimum log level be checked - on the `Logger` before creating `LogMessage`, or on each `LogAppender` independently? Arguments for Logger-side: avoid constructing `LogMessage` objects that will be discarded (performance). Arguments for Appender-side: different appenders can have different thresholds (file gets DEBUG, console gets WARN only). What does Python's stdlib choose, and does that change your answer?

### Related LLD Problems

|Problem|What transfers|
|---|---|
|**Observer / Event System**|`Logger` → `LogAppender` is publish/subscribe. Logger is the publisher, appenders are subscribers. The `additivity` + hierarchy is a tree-shaped pub/sub.|
|**Plugin / Extension System**|Same extensibility model — a `Protocol`-based interface (`LogAppender`) with concrete implementations registered at runtime. Identical to how IDE plugin systems work.|
|**Notification Service**|`LogAppender` maps directly to a notification channel (Email, SMS, Push). `LogLevel` maps to notification severity/priority. The routing and filtering logic is the same problem.|

### Connection to HLD Problems

Two direct HLD mappings:

**Centralised logging infrastructure** - At scale, `FileAppender` becomes a log shipper (Fluentd, Logstash) sending to a central store (Elasticsearch, CloudWatch). The LLD `LogAppender` interface is literally the abstraction boundary that makes this swap possible. The HLD question "how do you aggregate logs from 500 services?" starts with "each service has a logger that writes to a local buffer, which is drained to Kafka, which feeds the log store."

**Log levels as an operational lever** - In HLD, log verbosity is a runtime-configurable property (feature flag, config service). Prod runs at `WARN`, you flip it to `DEBUG` for 5 minutes to diagnose an incident, then flip back. The `Logger.level` field being mutable (not final/frozen) is what enables this - it's an intentional design choice, not an oversight.

Example Code : https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/loggingframework