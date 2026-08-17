import json
import boto3
from moto import mock_aws


def setup_registrations_table():
    dynamodb = boto3.resource(
        "dynamodb",
        region_name="us-east-1"
    )

    return dynamodb.create_table(
        TableName="Registrations",
        KeySchema=[
            {"AttributeName": "eventId", "KeyType": "HASH"},
            {"AttributeName": "registrationId", "KeyType": "RANGE"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "eventId", "AttributeType": "S"},
            {"AttributeName": "registrationId", "AttributeType": "S"}
        ],
        BillingMode="PAY_PER_REQUEST"
    )


@mock_aws
def test_register_attendee_valid_input():
    setup_registrations_table()

    from register_attendee import app

    event = {
        "pathParameters": {
            "id": "event-123"
        },
        "body": json.dumps({
            "name": "Jane Doe",
            "email": "jane@example.com"
        })
    }

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 201

    body = json.loads(response["body"])

    assert body["eventId"] == "event-123"
    assert "ticketCode" in body


@mock_aws
def test_register_attendee_missing_email():
    setup_registrations_table()

    from register_attendee import app

    event = {
        "pathParameters": {
            "id": "event-123"
        },
        "body": json.dumps({
            "name": "Jane Doe"
        })
    }

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 400