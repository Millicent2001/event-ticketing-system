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
def test_get_registration_found():
    table = setup_registrations_table()

    table.put_item(
        Item={
            "eventId": "event-123",
            "registrationId": "reg-456",
            "name": "Jane Doe"
        }
    )

    from get_registration import app

    event = {
        "pathParameters": {
            "id": "reg-456"
        }
    }

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 200

    body = json.loads(response["body"])

    assert body["registrationId"] == "reg-456"


@mock_aws
def test_get_registration_not_found():
    setup_registrations_table()

    from get_registration import app

    event = {
        "pathParameters": {
            "id": "does-not-exist"
        }
    }

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 404