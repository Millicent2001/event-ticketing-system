import json
import boto3
from moto import mock_aws


@mock_aws
def test_list_events_returns_items():
    dynamodb = boto3.resource(
        "dynamodb",
        region_name="us-east-1"
    )

    table = dynamodb.create_table(
        TableName="Events",
        KeySchema=[
            {"AttributeName": "eventId", "KeyType": "HASH"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "eventId", "AttributeType": "S"}
        ],
        BillingMode="PAY_PER_REQUEST"
    )

    table.put_item(
        Item={
            "eventId": "123",
            "name": "Test Event",
            "date": "2026-01-01",
            "capacity": 50
        }
    )

    from list_events import app

    response = app.lambda_handler({}, None)

    assert response["statusCode"] == 200

    body = json.loads(response["body"])

    assert len(body["events"]) == 1
    assert body["events"][0]["name"] == "Test Event"


@mock_aws
def test_list_events_empty_table():
    dynamodb = boto3.resource(
        "dynamodb",
        region_name="us-east-1"
    )

    dynamodb.create_table(
        TableName="Events",
        KeySchema=[
            {"AttributeName": "eventId", "KeyType": "HASH"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "eventId", "AttributeType": "S"}
        ],
        BillingMode="PAY_PER_REQUEST"
    )

    from list_events import app

    response = app.lambda_handler({}, None)

    assert response["statusCode"] == 200

    body = json.loads(response["body"])

    assert body["events"] == []