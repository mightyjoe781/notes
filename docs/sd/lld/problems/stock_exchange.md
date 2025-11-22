# Stock Exchange

Problem Link : https://leetcode.com/discuss/post/3636431/phone-pe-machine-coding-stock-exchange-b-x05o/

Important Point/Solution Requirements from above question:

- Storage: In Memory
- Interaction: REST API
- Nature: Flows should be running end-end & Clean Code

Functional Requirements

- System should allow users to create, modify a trade order, check status of the trade order and execute (match) (CRUD) the order.
- Buy orders should be matched with sell orders based on an exact price match and FIFO ordering
- Concurrency to be kept in mind
- Maintain an orderbook per symbol which holds all the current unexecuted orders

Extra Requirements

- Trade should be cancelled if not executed within a specified time (Trade Expiry)

## Class Diagrams

A initial draft could be something like this from a very high level approach

![](assets/Pasted%20image%2020251122232939.png)

Lets refactor this and all the classes & read the question. Trade will be a matched order i.e. when a seller is met with a buyer or vice-versa, we get a trade. Notice Entity classes are already given in the question.

### Correct Design

![](assets/Pasted%20image%2020251122234425.png)

### Service Layer Design

There could be multiple types of Order Matching Strategies

![](assets/Pasted%20image%2020251123002448.png)

### Controllers

![](assets/Pasted%20image%2020251123003331.png)

### Exception Classes

![](assets/Pasted%20image%2020251123003530.png)


Example Code: 



