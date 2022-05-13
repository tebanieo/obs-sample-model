import boto3

dynamodb = boto3.client("dynamodb")

try:
    dynamodb.create_table(
        TableName="online-banking",
        AttributeDefinitions=[
            {"AttributeName": "PK", "AttributeType": "S"},
            {"AttributeName": "SK", "AttributeType": "S"},
        ],
        KeySchema=[
            {"AttributeName": "PK", "KeyType": "HASH"},
            {"AttributeName": "SK", "KeyType": "RANGE"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    print("Table created successfully.")
except Exception as e:
    print("Could not create table. Error:")
    print(e)
