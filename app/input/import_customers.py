import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("online-banking")

customers = []

with open("final_customers.json", "r") as file:
    for row in file:
        customers.append(json.loads(row))

with table.batch_writer() as batch:
    for item in customers:
        batch.put_item(Item=item)
