import json
import boto3
import random

# dynamodb = boto3.resource("dynamodb")
# table = dynamodb.Table()
shards = 4
customers = []
accounts = []
account_customer = {}
final_customers = []

with open("other_files/medium_batch_customer.json", "r") as file:
    for row in file:
        customers.append(json.loads(row))

for customer in customers:
    for account in customer["accounts"]:
        accounts.append(account["account_id"])
        account_customer[account["account_id"]] = customer["customer_id"]

for customer in customers:
    final_customers.append(
        {
            "PK": "C#" + customer["customer_id"],
            "SK": "#META#",
            "address": customer["address"],
            "customer_id": customer["customer_id"],
        }
    )
    for account in customer["accounts"]:
        final_customers.append(
            {
                "PK": "C#" + customer["customer_id"],
                "SK": "A#" + account["account_id"],
                "account_id": account["account_id"],
                "account_name": account["account_name"],
            }
        )

with open("input/final_customers.json", "w") as output:
    for item in final_customers:
        output.write(json.dumps(item) + "\n")


batch_transactions = []
final_transactions = []

with open("other_files/tx_input.json", "r") as tx1:
    for transaction in tx1:
        batch_transactions.append(json.loads(transaction))

for transaction in batch_transactions:
    for operation in transaction["operations"]:
        # print(operation)
        operation_builder = {
            "PK": "C#" + account_customer[operation["account_id"]],
            "SK": transaction["date"]
            + "#"
            + operation[
                "operation_id"
            ],  #  # what does this means? for the access patterns? What happens if we have A#account_id#date instead or A#account_id#date#operation?
            "customer_id": account_customer[operation["account_id"]],
            "account_id": operation["account_id"],
            "operation_id": operation["operation_id"],
            "amount": operation["amount"],
            "transaction_id": transaction["transaction_id"],
            "date": transaction["date"],
            "GSI1PK": "C#" + account_customer[operation["account_id"]],
            "GSI1SK": transaction[
                "date"
            ],  # Why I don't have to include more information here?
        }
        if len(transaction["operations"]) == 1:
            operation_builder["transaction_type"] = "SCHEDULED_PAYMENT"
            operation_builder["GSI2PK"] = str(random.randint(1, shards))
            operation_builder["GSI2SK"] = transaction["date"]

        final_transactions.append(operation_builder)

# # print(final_transactions)
with open("input/final_tx_transactions.json", "w") as output:
    for item in final_transactions:
        output.write(json.dumps(item) + "\n")
