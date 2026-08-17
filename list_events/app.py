import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Events")


def lambda_handler(event, context):
    response = table.scan()
    events = response.get("Items", [])

    return {
        "statusCode": 200,
        "body": json.dumps({"events": events})
    }