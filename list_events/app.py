import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Events")


def lambda_handler(event, context):
    response = table.scan()
    events = response.get("Items", [])

    return {
        "statusCode": 200,
        "body": json.dumps(
            {"events": events},
            default=lambda o: float(o) if isinstance(o, Decimal) else o
        )
    }