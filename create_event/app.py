import json
import uuid
from datetime import datetime


def lambda_handler(event, context):

    body = json.loads(event.get("body", "{}"))

    event_name = body.get("eventName")
    description = body.get("description")
    location = body.get("location")
    event_date = body.get("eventDate")

    if not event_name:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "eventName is required"
            })
        }

    new_event = {
        "eventId": str(uuid.uuid4()),
        "eventName": event_name,
        "description": description,
        "location": location,
        "eventDate": event_date,
        "createdAt": datetime.utcnow().isoformat()
    }

    return {
        "statusCode": 201,
        "body": json.dumps({
            "message": "Event created successfully",
            "event": new_event
        })
    }