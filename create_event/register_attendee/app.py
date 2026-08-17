import json
import uuid
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Registrations")


def lambda_handler(event, context):
    event_id = event["pathParameters"]["id"]

    body = json.loads(event["body"])
    name = body.get("name")
    email = body.get("email")

    if not name or not email:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "name and email are required"
            })
        }

    registration_id = str(uuid.uuid4())
    ticket_code = str(uuid.uuid4())[:8].upper()

    table.put_item(
        Item={
            "eventId": event_id,
            "registrationId": registration_id,
            "name": name,
            "email": email,
            "ticketCode": ticket_code
        }
    )

    return {
        "statusCode": 201,
        "body": json.dumps({
            "registrationId": registration_id,
            "eventId": event_id,
            "name": name,
            "email": email,
            "ticketCode": ticket_code
        })
    }