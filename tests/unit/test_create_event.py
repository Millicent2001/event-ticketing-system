import json
from create_event import app


def test_create_event_valid_input():
    event = {
        "body": json.dumps({
            "eventName": "Tech Meetup",
            "description": "Technology networking event",
            "location": "Accra",
            "eventDate": "2026-09-01"
        })
    }

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 201

    body = json.loads(response["body"])

    assert body["message"] == "Event created successfully"
    assert "event" in body
    assert body["event"]["eventName"] == "Tech Meetup"
    assert "eventId" in body["event"]


def test_create_event_missing_event_name():
    event = {
        "body": json.dumps({
            "description": "Technology networking event",
            "location": "Accra",
            "eventDate": "2026-09-01"
        })
    }

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 400

    body = json.loads(response["body"])

    assert body["message"] == "eventName is required"