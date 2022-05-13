# DynamoDB online banking data modelling

This is a workshop that intends to cover many of the DynamoDB data modelling scenarios, this workshop is inspired on some online banking migrations that have been completed in the past years but its a mix and match of several different real customer experiences. The major intent for this workshop is to educate around data modelling and how to de-normalize your data, and work with Amazon DynamoDB.

# Octank Banking

Octank Banking is an APJ based institution that has over 40+ million users, it is one of the largest institutions in the region serving customers from over 20 years. 

The Octank banking institution is planing to launch their new online banking mobile application. The architecture team has been very worried about this new change since the Mainframe/System of record is already over pressure, the customer has choosen to go with a cloud native application running in AWS to overcome the problem of escale. The customer is expecting this application to be a great success and traffic can arrive from different regions across the APJ region. 

The main objective of this application is to offload the sytem of record and allow the users to have a seameless experience while navigating on the app. In the initial phase the transactions are served by the system of record, and the application in AWS will need to send the information back to their datacenter. 
 

 ## Background - Access Patterns -  Data description

 The migration will happen in two ways, the old transactions will be imported from the system of record in batches.
 The second phase includes a real time replication between the mainframe and the AWS cloud so customers can validate their transactions in near-real time. 

 The system of records will send the information per transaction. 

 One transaction is the result of an activity that happens between two parties, for example when a customer pays the credit card, the money is originated from one account and sent to another account (the credit card one), if the destination account is an external party it should be flagged as external?. The exception to this rule are `DEPOSIT` and `WITHDRAWAL` since the deposits assumes the money comes/is taken from cash from an ATM or a branch.

 There might be scenarios where transactions span multiple accounts, for example customers can choose to pay bills from their savins and every day account to pay their credit card, line of credit or morgage.
 When the transactions span multiple accounts the result amount of the transaction must be 0. For example, you pay a bill from your savings account -$100 but you transfer the money to the merchant $100, at the end of the day the total amount of the transaction is 0.

Customers will be presented with a welcome page with their accounts name, number and balance up to date (With the date of the last transaction on top), however it should not present transaction details at this point. 
When the customer opens each account it should present the last 30 operations starting with the most recent ones.
Customers have the option to search for transactions that occured during an specific period of time, for example between two date ranges.

Customers and security requires to query transactions by transaction ID, this query should return all the parties that were involved in a transaciton, for this the customer can click on the transaction ID available at the account detail, or they can just type the exact transaction id. 

There is been some incidents where security wants to automatically suspend cards based on suspicious activity and deliver an SMS to customers, the initial scope for this is to flag transactions from the same account that occurred in different cities during the same 30 minute window. For example a credit card transaction in person from Sydney and then another transaction in person in Melbourne within 15 minutes. 


## Incoming Data format
Each transaction generates one operation_id per account (this what would happend if we don't have this unique operation_id), and the same transaction can occur in different accounts as explained in the section above.

To simplify processing logic during this workshop we will assume the data is received per transaction, so we will have the entire transaction in JSON format, one object per account:


```JSON
{
    "customer_id":"4082-82388216-2310",
    "first_name":"Osborn",
    "last_name":"Braidford",
    "email":"obraidford0@eepurl.com",
    "address":{
        "street_address":"7641 Pine View Pass",
        "postal_code":"357-0211",
        "city":"Morohongō",
        "country":"Japan"
        },
    "accounts":[
        {
            "account_id":"419-653249-8586",
            "account_name":"Credit Titanium"
        },
        {
            "account_id":"517-513534-1146",
            "account_name":"Every Day"
        },
        {
            "account_id":"056-932264-9238",
            "account_name":"Credit Black"
        }
    ]
}
```

To simplify processing logic during this workshop we will assume the data is received per transaction, so we will have the entire transaction in JSON format, one object per account:

```JSON
{
    "transaction_id":"11932-49801-07082-53869",
    "operations":[
        {
            "account_id":"349-552407-2873",
            "operation_id":"5530-483520-822449-4592",
            "amount":3578
        },
        {
            "account_id":"505-816979-3351",
            "operation_id":"0092-913394-407864-3714",
            "amount":2707
        }
    ],
    "date":"2022-03-16T09:31:51Z"
}
```


## Authors and acknowledgment
This workshop was created by Esteban Serna trying to help banking and financial customers to understand NoSQL design patterns, and how to approach a denormalization exercise. 

## License
Not open source, but I need to identify the license :) 

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
