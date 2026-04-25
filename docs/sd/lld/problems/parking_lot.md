# Design Parking Lot System

## Requirements

- N floors, each with configurable slots for cars, bikes, electric cars, electric bikes
- Slot numbers increase with distance from entry (nearest = lowest number)
- On entry: capture registration number + color, assign nearest valid slot, issue ticket
- On exit: unpark vehicle, compute fee, accept payment (cash / card / FastTag / UPI)
- Pricing is per-hour and differs by vehicle type; electric vehicles have a charge component
- A bike can park in any nearest empty slot; a car can only park in a car slot
- Queries: find vehicle by spot, find spot by vehicle number, find all vehicles/spots by color

## Functionalities

1. `park(vehicle)` → assign nearest valid slot, return ticket
2. `unpark(ticket)` → release slot, compute fare, process payment
3. `getVehicleAtSlot(slotNumber, floor)` → return vehicle
4. `getSlotByVehicleNumber(regNumber)` → return slot
5. `getRegNumbersByColor(color)` → list of registration numbers
6. `getSlotsByColor(color)` → list of slot numbers

## Design Patterns at Play

Call these out early - it signals you know _why_ the design looks the way it does.

|Pattern|Where Used|Why|
|---|---|---|
|Strategy|`FindAvailableSlotStrategy`|Swap linear/priority-queue slot-finding without touching the manager|
|Strategy|`PriceCalculationStrategy`|Each strategy is composable; a ticket can carry multiple (hourly + electric charge)|
|Strategy|`PaymentStrategy`|Decouple payment method from checkout logic|
|Abstract Class|`ParkingSlot`, `Vehicle`|Shared state + partial implementation; concrete types extend|
|Interface / Protocol|`ChargableVehicle`, `CarSlot`, `ElectricSlot`, `BikeSlot`|Capability mix-ins; multiple inheritance without the diamond problem|
|Factory|Slot/Vehicle creation|Caller asks for "an electric car slot" without knowing the concrete type|
|Singleton|`ParkingLot`|One lot per system instance|
|Builder|`Ticket` construction|Many optional fields (exitTime, paymentStrategy); skip in short interviews|

## Class Design

### Vehicle Hierarchy

`Vehicle` is abstract with `regNumber`, `color`, `vehicleType (enum)`. `Car` and `Bike` extend it directly.

`ElectricCar` and `ElectricBike` extend `Vehicle` **and** implement `ChargableVehicle` interface - that interface adds `charge()` and `getBatteryPercent()`. This is the classic "capability interface" pattern: you don't want `charge()` on all vehicles, only the ones that need it.

```
Vehicle (abstract)
├── Car
├── Bike
├── ElectricCar  ──implements──> ChargableVehicle
└── ElectricBike ──implements──> ChargableVehicle
```

![](assets/Pasted%20image%2020251119112638.png)

### Parking Slot Hierarchy

**First design** : Each concrete slot type (e.g. `CarParkingSlot`) inherits from both `ParkingSlot` abstract class and a capability interface (`CarSlot`, `ElectricSlot`, `BikeSlot`). `park()` is on `CarSlot`, `parkBike()` on `BikeSlot`, `chargeVehicle()` on `ElectricSlot`. Problem: `park()` is split across interfaces with different names, making the manager awkward.

![](assets/Pasted%20image%2020251119112615.png)

**Revised design**: Pull `park()` up into `ParkingSlot` itself (it becomes a concrete method on the abstract class, or an abstract method all subclasses implement). Now the manager can call `slot.park(vehicle)` uniformly. Also adds `supportedVehicleType` (a list/set of `VehicleType` enum values) to `ParkingSlot` - this is what lets the slot-finding strategy filter eligibility without downcasting.

![](assets/Pasted%20image%2020251119112919.png)

**Use the revised design.** The key improvement is: slot eligibility check becomes `vehicle.vehicleType in slot.supportedVehicleTypes` rather than `isinstance(slot, CarSlot)`.

Concrete slot types: `CarParkingSlot`, `BikeParkingSlot`, `ElectricCarParkingSlot`, `ElectricBikeParkingSlot`.

![](assets/Pasted%20image%2020251119113321.png)

### ParkingLot + ParkingFloor

```
ParkingLot (Singleton)
  └── List[ParkingFloor]
        └── List[ParkingSlot]
```

`ParkingFloor` has `floorNumber` and its list of slots. `ParkingLot` holds the floors and a reference to `ParkingLotManagerSVC` (the orchestrator).

### Ticket

First and foremost, we will require a payment slip or ticket, along with that we will need various Pricing strategy like time or dynamic or type of vehicle.

```
Ticket
  entryTime: datetime
  exitTime: datetime | None
  vehicle: Vehicle
  parkingSlot: ParkingSlot
  priceStrategies: list[PriceCalculationStrategy]   # composition
  paymentStrategy: PaymentStrategy | None           # composition, set at exit
```

Two separate Strategy interfaces hang off `Ticket`:

**`PriceCalculationStrategy`** - `calculatePrice(ticket) -> int` (always int, paise/cents)  
Concrete: `HourlyPricingStrategy`, `CarHourlyPricingStrategy`, `BikeHourlyPricingStrategy`, `ConstantPriceStrategy`, `CarValetPricingStrategy`, `ElectricChargePricingStrategy`

The diagram's note is important: `CarHourlyPricingStrategy` and `BikeHourlyPricingStrategy` do **not** inherit from `HourlyPricingStrategy`. 

They both implement `PriceCalculationStrategy` directly. Reason: you'd need concrete classes anyway (since hourly rate differs), and multiple inheritance in Python with concrete base classes gets messy. Keep the hierarchy flat.

Total fare = `sum(s.calculatePrice(ticket) for s in ticket.priceStrategies)`. Composability is the point - an electric car gets `[CarHourlyPricingStrategy(), ElectricChargePricingStrategy()]`.

**`PaymentStrategy`** - `pay(amount: int) -> bool`  

Concrete: `CreditCard`, `UPI`, `FastTag`

![](assets/Pasted%20image%2020251119114108.png)

![](assets/Pasted%20image%2020251119114512.png)
### ParkingLotManager

```
ParkingLotManager
  findAvailableSlotStrategy: FindAvailableSlotStrategy
  
  doParking(vehicle) -> Ticket
  leaveFromParking(ticket, paymentStrategy) -> int   # returns amount paid
```

This is the orchestrator. It delegates slot-finding to the strategy (linear scan, nearest-first priority queue, etc.) and delegates payment to whatever strategy is passed at exit.

`FindAvailableSlotStrategy` is a separate Strategy interface - `findSlot(floors, vehicleType) -> ParkingSlot | None`. Swapping this doesn't touch any other class.

![](assets/Pasted%20image%2020251119114519.png)

## Flow: Park and Unpark

**Park:**

1. `ParkingLotManager.doParking(vehicle)` called
2. Strategy finds nearest eligible slot → `slot.park(vehicle)` sets slot status to `OCCUPIED`
3. Create `Ticket(entryTime=now, vehicle=vehicle, slot=slot, priceStrategies=[...])`
4. Return ticket

**Unpark:**

1. `leaveFromParking(ticket, paymentStrategy)` called
2. Set `ticket.exitTime = now`
3. Compute total fare: `sum(s.calculatePrice(ticket) for s in ticket.priceStrategies)`
4. `paymentStrategy.pay(fare)`
5. `slot.status = AVAILABLE`, clear vehicle reference
6. Return fare paid

## Slot Status

`ParkingSlot.status` is an enum: `AVAILABLE | OCCUPIED | RESERVED | OUT_OF_SERVICE`

State transitions:

```
AVAILABLE ──park()──> OCCUPIED ──unpark()──> AVAILABLE
AVAILABLE ──reserve()──> RESERVED ──confirm()──> OCCUPIED
ANY ──disable()──> OUT_OF_SERVICE
```

The slot itself enforces valid transitions - `park()` should raise if status isn't `AVAILABLE`.

## Python Supplement


```python
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Protocol


class VehicleType(Enum):
    CAR = auto()
    BIKE = auto()
    ELECTRIC_CAR = auto()
    ELECTRIC_BIKE = auto()


class SlotStatus(Enum):
    AVAILABLE = auto()
    OCCUPIED = auto()
    OUT_OF_SERVICE = auto()


# --- Capability interface, not base class ---
class ChargableVehicle(Protocol):
    def charge(self) -> None: ...
    def get_battery_percent(self) -> int: ...


# --- Vehicle hierarchy ---
@dataclass
class Vehicle(ABC):
    reg_number: str
    color: str
    vehicle_type: VehicleType


@dataclass
class ElectricCar(Vehicle, ChargableVehicle):
    battery_percent: int = 0
    def __post_init__(self): self.vehicle_type = VehicleType.ELECTRIC_CAR
    def charge(self) -> None: self.battery_percent = 100
    def get_battery_percent(self) -> int: return self.battery_percent


# --- Strategy: pricing (the tricky part — composable, flat hierarchy) ---
class PriceCalculationStrategy(Protocol):
    def calculate_price(self, entry: datetime, exit: datetime) -> int: ...  # always int (paise)

@dataclass
class HourlyPricingStrategy:
    rate_per_hour: int  # in paise, never float
    def calculate_price(self, entry: datetime, exit: datetime) -> int:
        hours = max(1, int((exit - entry).total_seconds() // 3600))
        return hours * self.rate_per_hour


# --- Slot: status transition lives HERE, not in manager ---
@dataclass
class ParkingSlot(ABC):
    slot_number: int
    floor_number: int
    supported_types: set[VehicleType]
    status: SlotStatus = SlotStatus.AVAILABLE
    vehicle: Vehicle | None = None

    def park(self, vehicle: Vehicle) -> None:
        if self.status != SlotStatus.AVAILABLE:
            raise ValueError(f"Slot {self.slot_number} not available")
        if vehicle.vehicle_type not in self.supported_types:
            raise ValueError(f"Vehicle type {vehicle.vehicle_type} not supported")
        self.vehicle = vehicle
        self.status = SlotStatus.OCCUPIED

    def unpark(self) -> Vehicle:
        if self.status != SlotStatus.OCCUPIED or self.vehicle is None:
            raise ValueError("Slot is not occupied")
        v, self.vehicle = self.vehicle, None
        self.status = SlotStatus.AVAILABLE
        return v


# --- FindAvailableSlot strategy ---
class FindAvailableSlotStrategy(Protocol):
    def find(self, floors: list, vehicle_type: VehicleType) -> ParkingSlot | None: ...

class NearestSlotStrategy:
    """Linear scan; slots on lower floors / lower numbers come first."""
    def find(self, floors: list, vehicle_type: VehicleType) -> ParkingSlot | None:
        for floor in floors:
            for slot in sorted(floor.slots, key=lambda s: s.slot_number):
                if slot.status == SlotStatus.AVAILABLE and vehicle_type in slot.supported_types:
                    return slot
        return None

# Deliberately left as exercise:
# - Ticket dataclass with entry/exit time and fare computation
# - ParkingLotManager.do_parking / leave_from_parking
# - PaymentStrategy Protocol + CreditCard / UPI / FastTag implementations
# - ParkingLot singleton wiring floors + manager
```

---

## Further Reading & Exercises

### Directly Relevant

- _Head First Design Patterns_ - Chapter 1 (Strategy), Chapter 3 (Decorator, relevant if you want composable slot capabilities)
- _Refactoring_ (Fowler) - "Replace Conditional with Polymorphism" - exactly what the slot hierarchy does for vehicle-type dispatch
- Python `abc` module docs: [https://docs.python.org/3/library/abc.html](https://docs.python.org/3/library/abc.html) - ABC vs Protocol, when to use each
- Python `enum` docs - `Enum(auto())`, using enums as set members for `supported_types`: [https://docs.python.org/3/library/enum.html](https://docs.python.org/3/library/enum.html)
- Real parking systems use event sourcing for slot state - AWS blog "Event Sourcing Pattern" is a good read for the HLD angle

### Exercises

**Easy** - Implement `getSlotsByColor(color)` on `ParkingLot`. It needs to scan all floors and slots. Where does this method live - `ParkingLot`, `ParkingFloor`, or `ParkingLotManager`? Is there a meaningful difference?

**Medium** - Implement TTL-based slot reservation: a slot can be `RESERVED` for 15 minutes before a car arrives. If the car doesn't arrive, it flips back to `AVAILABLE`. Where does the timer live? Hint: you probably want a background thread or a lazy-expiry check in `find()`.

**Hard (no single right answer)** - The `FindAvailableSlotStrategy` currently does a flat scan. Now you need to support "nearest to a specific entry gate" where the lot has multiple gates on different sides. Two approaches: (a) sort slots by Euclidean distance to the gate at query time, or (b) pre-compute a priority queue per gate. What does each cost in terms of memory and update complexity when a slot's status changes? Argue both sides.

### Related Problems

- **Hotel Room Booking** - same slot-availability + assignment core, adds date-range queries and overbooking logic; the `FindAvailableSlotStrategy` pattern transfers directly
- **Elevator System** - `SlotStatus` state machine maps cleanly to elevator states (IDLE, MOVING_UP, MOVING_DOWN); the Strategy pattern reappears for floor-selection algorithms
- **Library Management System** - same "find available copy, issue ticket (borrow record), return and update status" loop; pricing becomes late-fee calculation

### Connection to HLD

- **Large-Scale Parking / Smart City** - at HLD you'd split this into a real-time slot availability service (writes on every park/unpark, needs low latency) and a reporting/query service (color queries, occupancy stats). The LLD's clean separation of `ParkingSlot` state from `ParkingLotManager` queries directly maps to the CQRS split at HLD.
- **Ride-hailing dispatch** - `FindAvailableSlotStrategy` is structurally identical to the driver-matching problem: find the nearest available resource of the right type. At HLD scale this becomes a geo-indexed query (PostGIS, S2 geometry).
- **Event ticketing (BookMyShow)** - same "reserve → confirm → expire if not paid" lifecycle; the `RESERVED` slot state here is the seat-hold pattern there.