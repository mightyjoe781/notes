# Design Stock Broker

- There are two terminologies that needs to be cleared,
    - Stock Exchange - e.g. NSE/BSE
        - Lists Stocks
        - Order Matching
    - Stock Broker ~ eg. Groww, Zerodha
        - Helps users participate to Stock Exchange trades
        - Read Prices from Stock Exchanges
        - Accept orders on Behalf of Users and pass them to Exchanges

Problem Statement

- We might be having multiple exchanges who are sending us the new price data of the stock (NSE, BSE etc)
- Design a broker which can take the stock symbol and price from exchanges and show you the latest price of the stock.
- Good to have feature -› we should be able to store historical price of the stock (expected to be implementation)

Requirements

- No API exposure required, cli running the code
- In-memory storage should be ok
- we expect an end to end running solution

## Class Design

### StockExchange & Subscriber Class Design

Following diagram outlines an Observer Pattern for implementing above question, start with following classes to implement the solution.

![](assets/Pasted%20image%2020251121114652.png)

Example Code : https://github.com/singhsanket143/StockBrokerLLD-Problem

