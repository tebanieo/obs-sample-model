import boto3

dynamodb = boto3.client("dynamodb")

try:
    dynamodb.update_table(
        TableName="online-banking",
        AttributeDefinitions=[
            {"AttributeName": "GSI1SK", "AttributeType": "S"},
            {"AttributeName": "GSI1PK", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexUpdates=[
            {
                "Create": {
                    "IndexName": "GSI1",
                    "KeySchema": [
                        {"AttributeName": "GSI1PK", "KeyType": "HASH"},
                        {"AttributeName": "GSI1SK", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                }
            }
        ],
    )
    print("Table updated successfully.")
except Exception as e:
    print("Could not update table. Error:")
    print(e)
