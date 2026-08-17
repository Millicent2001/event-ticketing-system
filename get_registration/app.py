import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Registrations")


def lambda_handler(event, context):
    registration_id = event["pathParameters"]["id"]

    response = table.scan(
        FilterExpression="registrationId = :rid",
        ExpressionAttributeValues={
            ":rid": registration_id
        }
    )

    items = response.get("Items", [])

    if not items:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "error": "Registration not found"
            })
        }

    return {
        "statusCode": 200,
        "body": json.dumps(items[0])
    }