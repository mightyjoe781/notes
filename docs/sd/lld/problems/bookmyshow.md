# Design BookMyShow

There could be multiple variant of the problems, any kind of the booking system requires a resource contention, basically multiple users should not get the same seat or if some user is in the process of booking seat (payments etc) don't give his selected seat to others.

There are primarily two ways to deal with this problems using Locks

- Pessimistic Lock ~ acquire lock before proceeding with the txn
- Optimistic Lock ~ maintain internal version of the rows

More Details here : [RDBS System Design](../../hld/advanced/relational_database.md)

## Requirements

- Proper DB Integration
- REST API
- Working Booking Flow

## Class Design

### Movie Class

![](assets/Pasted%20image%2020251120001835.png)

### Theatre Class

![](assets/Pasted%20image%2020251120001942.png)

Since there could be multiple shows where a seat belongs to that specific seat, we create a joined table called as ShowSeat.

![](assets/Pasted%20image%2020251120002338.png)
### Ticket Entity

![](assets/Pasted%20image%2020251120003218.png)


Project Code : https://github.com/singhsanket143/LLD-BookMyShow