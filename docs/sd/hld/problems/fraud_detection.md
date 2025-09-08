# Designing Fraud Detection

Motive : Designing systems using Big-Data Technologies

Requirements:
Financial Transaction are risky and prone to frauds. Banks have to deploy fraud detection system, that can

- detect fraud in realtime
- block the transaction
- inform a customer support executive (to take consent)

![](assets/Pasted%20image%2020250908073701.png)

When user initiates the transaction, the bank makes an entry but before proceeding further, it checks for a potential fraud, if not a fraud : allow the transaction
otherwise : hold the transaction, involve the executive, call the customer and confirm, if customer says yes : allow the transaction, else abort the txn.

### Storage
We need an ability to register a transaction.
Schema


| source_acc | target_acc | status | ...(ip, region, location, target_bank, etc.) |
| ---------- | ---------- | ------ | -------------------------------------------- |
|            |            |        |                                              |

Target could be : `INITIATED/BLOCKED/FRAUD/ALLOWED/DONE/FAILED`

Given the schema is simple enough choice of DB is not that complex, we start with relational. Data is also shardable.
We can drop foreign key constraints here !
### Bank API (Txn API)
Bank API : is a set of servers behind load balancer.

![](assets/Pasted%20image%2020250908074553.png)

Transaction Handler (`http req`)

- get source and target entry
- extract details like `(ip, location, user agent)`
- send these details (synchronously) to fraud detection.

Fraud Detection is a simple HTTP based service that

- gets transaction and request details (over http)
- it returns if it is fraudulent or not

NOTE: Fraud detection service should respond within 200 ms
### Fraud Detection Algorithm (Decision trees/Random Forest)

Fraud Detection Service uses multiple parameters to judge if current transaction is fraud or not
We generate a lot of decision trees (random forests) from the training data and train the model. Every transaction is classified into either fraudulent or non fraudulent.

![](assets/Pasted%20image%2020250908075054.png)

NOTE: every new txn is classified across all & majority is considered.

### Preparing the data for training

Who knows which transaction were fraud ?
Customer support and Complaint Portal
We need to fetch transaction that had some fraud dispute.

![](assets/Pasted%20image%2020250908075508.png)

We write a job that periodically processes the data from the CS Database extract the fraud transactions, communication summary, details shared on the ticket.
Put them in a blob storage like S3

We use big data processing tools like Spark to move data to S3

![](assets/Pasted%20image%2020250908075620.png)

The amount of data moved from DB to S3 is huge and hence we need distributed computing.
One machine reading from S3 and transforming and writing to S3 will slow down the system.

To train our model, we need data, the details about the transaction
- who sent to whom
- from which ip, location, region, currency, etc. (these should be present in txn DB)

Similar to moving data from CS DB to S3 we used spark, we will move data from S3.

![](assets/Pasted%20image%2020250908080246.png)

Now that all the data we want to train model, is in S3
We use any distributed ML processing libraries to build the model. e.g. Using Spark + MLLib to train our *decision tree* & put the model back in S3.(just a file holding the serialized version of decision tree).
### Fraud Detection using the model

Fraud detection service is simple HTTP Service that

- load the model from S3
- creates in-memory structure to classify the transactions
- exposes API to do this synchronously

The end user facing the transaction invokes Fraud Detection to understand if it is fraudulent or not.
If not then transaction proceeds.
If yes, customer service is involved & notification is sent to the user

![](assets/Pasted%20image%2020250908080725.png)

### Exercise

- write a small spark job that extracts data from DB and puts them on local disk in multiple json files
- understand and write a random forest classifier
- explore MLLib + spark to plug random forest

