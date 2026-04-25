# Design an ATM

### Problem Clarifications

Before starting, nail down scope with the interviewer:

- **Entity depth**: Do we implement stub entities (`Card`, `User`, `Account`) or full models?
- **Storage**: In-memory dicts/lists or a proper DB layer (SQLite, etc.)?
- **Transport**: Pure in-process function calls, or are we simulating HTTP API calls?

For this write-up: single-feature flow, in-memory store, no real network.

### Functional Requirements

- One transaction at a time per ATM (no concurrency)
- Start button initiates the flow; returns a unique `txn_id`
- Card insertion → PIN validation → amount entry → cash dispensing
- Cancellation is allowed at every stage _except_ during dispensing
- All state transitions are auditable (logged)

## Flow of ATM Machine

- Transaction Start
    - Action: User presses the *Start Transaction* button.
    - API Call: An API is triggered to start the transaction
        - The API returns a unique transaction ID to track the interaction
    - Next Step: User Proceeds or cancels
- Card Insertion
    - Action : User inserts the card into the machine
    - API Call : The card details are read and sent to an API for validation
    - Validation Flow:
        - If Valid Proceed to next steps (Enter Amount)
        - If Invalid
            - Stop the txn
            - Eject the card and return to initial state
- Enter Withdrawal Amount
    - Action: User enters the withdrawal amount on the machine
    - API Call:
        - Validate if entered amount can be dispensed or not
            - Validation Flow
            - If Valid : Proceed to cash dispensing
            - If Invalid:
                - Allow the user to cancel or re-enter the amount
- Cash Dispensing
    - Action : If the amount is valid, the ATM dispense the cash
    - API Call: Close the transaction and reset it for tracking purposes.
    - User Feedback : Display a confirmation message indication successful transaction completion.
- Cancellation Options
    - NOTE:
        - Before Card Insertion (API to stop txn)
        - After card insertion but before entering the amount (API call to stop the transaction and eject the card).
        - After entering amount but before cash dispensing.
    - Restricted Cancellation
        - Once cash dispensing has started the transactions cannot be canceled
- Transaction Closure
    - Action : After cash dispensing or cancellation, the transaction is finished
    - API Call:
        - Mark the transaction as completed or canceled
        - Record the transaction details for audit/logging
### State Machine

The ATM is modelled as a finite state machine. Each state is an enum value; valid transitions are the only operations the machine exposes.

![](assets/Pasted%20image%2020251215104845.png)

From above diagram we can see on a high level how ATM Machine will Work.

We should utilize State Design Pattern, where other classes will call the State Class to update states.
Create a State Interface and rest of the classes will implement the state interface.

Link to Example Code : [Link](https://github.com/singhsanket143/Design-Patterns/tree/master/src/ATMMachine_StateDesignPattern)

### API Surface (summary)

|Endpoint|Triggered by|Notes|
|---|---|---|
|`create_txn_id()`|Start button|Returns `txn_id`|
|`validate_card(card)`|Card insertion|Returns bool; on False → eject|
|`validate_amount(txn_id, amt)`|Amount entry|Checks balance + cassette capacity|
|`close_txn(txn_id)`|Post-dispense|Marks complete, records audit log|
|`cancel_txn(txn_id)`|Any cancel|Works pre-dispense only|

## Class Diagram

![](assets/Pasted%20image%2020251215235701.png)

![](assets/Pasted%20image%2020251216000440.png)

Some of the implementation details are left as exercise like, Card, User, Amount, ATM (will have amount + currency) etc.

## Code Example (State Pattern)

The Java version uses an interface with `IllegalStateException`. In Python, the equivalent is an ABC with a default `raise` implementation.

```python
from abc import ABC, abstractmethod
from enum import Enum, auto

class ATMState(Enum):
    READY_FOR_TXN               = auto()
    READ_CARD_DETAILS_AND_PIN   = auto()
    READING_WITHDRAWAL_DETAILS  = auto()
    DISPENSE_CASH               = auto()
    EJECTING_CARD               = auto()
```


```python
class State(ABC):
    """
    Abstract base for every ATM state.
    Only override the methods that make sense for a given state.
    Everything else raises InvalidStateError by default.
    """

    def init_transaction(self) -> int:
        raise InvalidStateError(self)

    def read_card_details(self, card: "Card") -> bool:
        raise InvalidStateError(self)

    def read_withdrawal_details(self, txn_id: int, amount: int) -> bool:
        raise InvalidStateError(self)

    def dispense_cash(self, txn_id: int) -> None:
        raise InvalidStateError(self)

    def eject_card(self) -> None:
        raise InvalidStateError(self)

    @abstractmethod
    def get_state(self) -> ATMState:
        ...
```

```python
class InvalidStateError(Exception):
    def __init__(self, state: State):
        super().__init__(
            f"Operation not permitted in state: {state.get_state().name}"
        )
```

### Concrete State - `ReadyForTxnState`

Only `init_transaction` and `eject_card` (cancel before card) are meaningful here.


```python
class ReadyForTxnState(State):
    def __init__(self, atm: "ATM", api: "BackendAPI"):
        self._atm = atm
        self._api = api          # BackendAPI is an interface → could be Flask, FastAPI, mock

    def init_transaction(self) -> int:
        txn_id = self._api.create_txn_id()
        self._atm.set_state(ReadCardState(self._atm, self._api, txn_id))
        return txn_id

    def eject_card(self) -> None:
        # cancel before card was inserted — no-op on the card, just log
        self._api.cancel_txn(txn_id=None)

    def get_state(self) -> ATMState:
        return ATMState.READY_FOR_TXN
```

The pattern for every other state is the same: implement _only_ the valid operations, let everything else bubble up via the base `raise`.

### ATM Context Class

External modules (UI, hardware drivers) only ever touch `ATM` - never a state class directly.


```python
class ATM:
    def __init__(self, atm_id: str, api: "BackendAPI"):
        self.atm_id = atm_id
        self._api   = api
        self._state: State = ReadyForTxnState(self, api)

    # --- public surface (delegates to current state) ---

    def init_transaction(self) -> int:
        return self._state.init_transaction()

    def read_card_details(self, card: "Card") -> bool:
        return self._state.read_card_details(card)

    def read_withdrawal_details(self, txn_id: int, amount: int) -> bool:
        return self._state.read_withdrawal_details(txn_id, amount)

    def dispense_cash(self, txn_id: int) -> None:
        self._state.dispense_cash(txn_id)

    def eject_card(self) -> None:
        self._state.eject_card()

    def current_state(self) -> ATMState:
        return self._state.get_state()

    # --- internal (called only by State subclasses) ---

    def set_state(self, state: State) -> None:
        self._state = state
```

`set_state` is intentionally not in the public API. States call it on `self._atm` during transitions.\

### `BackendAPI` Interface

Keeps the ATM logic decoupled from the transport layer. Swap in a real HTTP client or a mock for tests.


```python
from typing import Protocol

class BackendAPI(Protocol):
    def create_txn_id(self) -> int: ...
    def validate_card(self, card: "Card") -> bool: ...
    def validate_amount(self, txn_id: int, amount: int) -> bool: ...
    def close_txn(self, txn_id: int) -> None: ...
    def cancel_txn(self, txn_id: int | None) -> None: ...
```

Using `Protocol` (structural subtyping) instead of an ABC means you never need to inherit from it - any object with matching methods works. This is the idiomatic Python alternative to Java interfaces.

### Entities Left as Exercise

These are straightforward dataclasses - no tricky design needed:

```python
@dataclass
class Card:
    card_number: str
    expiry: str
    holder_name: str

@dataclass
class Account:
    account_id: str
    balance: int          # store in paise/cents to avoid float math

@dataclass
class CashUnit:
    denomination: int
    count: int

@dataclass
class ATMCassette:           # the cash magazine inside the ATM
    units: list[CashUnit]

    def total_cash(self) -> int:
        return sum(u.denomination * u.count for u in self.units)
```

### Key Design Decisions (Python-specific)

- **`Protocol` over ABC for `BackendAPI`** - duck typing, zero coupling to the interface definition
- **`Enum(auto())`** for state names instead of string constants - typo-safe, IDE-navigable
- **`dataclass` for value objects** (`Card`, `CashUnit`) - free `__repr__`, `__eq__`, no boilerplate
- **`int` for money** - never `float`; store in smallest denomination unit
- **Default `raise` in base `State`** - each concrete state only overrides what's valid; the rest self-documents as illegal transitions

## Further Reading and Exercises

**State Pattern**

- _Design Patterns_ (GoF) - Chapter on State. The ATM is literally the canonical example.
- _Head First Design Patterns_ - more accessible walkthrough of the same pattern

**Python-specific**

- [`typing.Protocol` docs](https://docs.python.org/3/library/typing.html#typing.Protocol) - understand structural subtyping vs nominal. Know when `Protocol` beats `ABC`.
- Real Python: _Python's `dataclasses` module_ - covers `field()`, `__post_init__`, frozen dataclasses (good for `Card` which shouldn't mutate)

### LLD Thinking

These are adjacent systems worth designing for practice - they share the same patterns (State, Strategy, Observer, Protocol-backed dependencies):

- **Vending machine** - nearly identical state machine, but adds inventory management and change-giving
- **Elevator controller** - State + a scheduling algorithm (SCAN/LOOK) for which floor to serve next
- **Parking lot** - less about state, more about polymorphism (`TwoWheeler`, `FourWheeler`) and a clean slot-allocation strategy