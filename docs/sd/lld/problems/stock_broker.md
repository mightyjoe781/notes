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



