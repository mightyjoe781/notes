# Design an ATM

Solution Requirements:

- Do we want to implement only the required entities or a complete running flow as well of a feature ?
- Do we need a dedicated DB interaction or just some in memory DB is fine ?
- DO we need to implement network api's for interaction to the system or just a program is enough.

Functional Requirements

- Single Transaction Support
- The system should allow only one transaction at a time for a particular user. No concurrent transaction start Buttons.
- The ATM should have a start button to initiate the transactions. Card Insertion
- Once the transaction starts the machine should prompt the user to insert their card. System should validate the card details upon insertions. Card Validations
- If the card is invalid, system should reject it and return to the user.
- After validating the card, the system should ask the user the withdrawal amount, The system should validate if the withdrawal amount can be dispensed based on account balance, and machine capacity.
- Allowed Scenarios for cancellation support
    - before inserting the card.
    - After being prompted to

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
    - API Call: Close the transaction and resent it for tracking purposes.
    - User Feedback : Display a confirmation message indication successful transaction completion.
- Cancellation Options
    - NOTE:
        - Before Card Insertion (API to stop txn)
        - After card insertion but before entering the amount (API call to stop the transaction and eject the card).
        - After entering amount but before cash dispensing.
    - Restricted Cancellation
        - Once cash dispensing has started the transactions cannot be canceled
- Transaction Clouser
    - Action : After cash dispensing or cancellation, the transaction is finished
    - API Call:
        - Mark the transaction as completed or canceled
        - Record the transaction details for audit/logging

### API Overview

- Start Transaction
- Cancel Transaction
- Validate Card
- Validate Amount
- Close Transaction

## State of ATM Machine

This is how transition of the device states happens.

![](assets/Pasted%20image%2020251215104845.png)

From above diagram we can see on a high level how ATM Machine will Work.

We should utilize State Design Pattern, where other classes will call the State Class to update states.
Create a State Interface and rest of the classes will implement the state interface.

Link to Example Code : [Link](https://github.com/singhsanket143/Design-Patterns/tree/master/src/ATMMachine_StateDesignPattern)

## Class Diagram

![](assets/Pasted%20image%2020251215235701.png)

![](assets/Pasted%20image%2020251216000440.png)

Some of the implementation details are left as exercise like, Card, User, Amount, ATM (will have amount + currency) etc.