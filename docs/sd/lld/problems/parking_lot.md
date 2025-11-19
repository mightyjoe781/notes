# Design Parking Lot System

Design Requirements:

- Design a parking lot system to support N cars/bikes
- Parking lot has a number associated, which increases as we go far from entry point
- Automated Ticketing should happen
- When a car comes we take color of the car and registration number of the car.
- Assign nearest slot number and also allow leaving the car from the lot
- Once the car leaves we work the slot available again
- A bike can be parked in any nearest empty spot.
- whereas a car can only be parked in nearest empty car spot.
- There are configurable number of slots for electric cars and bikes also.
- On exit user should be able to pay via cash, card, or the fasttag
- Support of multiple floors
- Pricing per hour diff for bikes and cars

Functionalities

1. Given a vehicle, we should be able to park it and get the ticket
2. Given a vehicle, we should be able to unpark it and pay
3. Given a spot you should be able to find the vehicle parked in it
4. Given a vehicle number, find the parking slot in which its parked in
5. Return registration numbers of all cars of a particular color is parked
6. Return all spots/slots numbers where cars of a particular color is parked


Guessing the design patterns in the problem statement which are directly visible, e.g. Strategy pattern for payments, Strategy for finding the slot (linear search, binary search etc), Factory classes for entities, Builder Pattern will be required as well (can be skipped in short interviews), Every parking slot will have states.

## Class Diagrams

### Vehicle Design

For cars we can design something like this: 

![](assets/Pasted%20image%2020251119112638.png)

### Parking Slot Design

Parking Slots can be designed as :

![](assets/Pasted%20image%2020251119112615.png)

We can move `park()` method to ParkingSlot Class because Now each Parking slot supports its own specific type of vehicle

![](assets/Pasted%20image%2020251119112919.png)

Now since according to problem, each ParkingLot will have multiple floors and those will contain the Parking Slots, we have following classes

![](assets/Pasted%20image%2020251119113321.png)

### Adding Pricing Strategy Classes

First foremost we will require a paymentslip or ticket, along with that we will need various Pricing strategy like time or dynamic or type of vehicle.

![](assets/Pasted%20image%2020251119114108.png)

### Parking Lot Manager

This will be responsible for orchestrating entire system.

![](assets/Pasted%20image%2020251119114519.png)

### Payment Startegy

![](assets/Pasted%20image%2020251119114512.png)
