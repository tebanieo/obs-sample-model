import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("online-banking")

transactions = []

with open("final_tx_transactions.json", "r") as file:
    for row in file:
        transactions.append(json.loads(row))

## What do we do here?

with table.batch_writer() as batch:
    for item in transactions:
        batch.put_item(Item=item)
