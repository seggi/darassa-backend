import os
import json
from twilio.rest import Client


ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
DEFAULT_SENDER = os.getenv('TWILIO_DEFAULT_SENDER')

client = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_bulk_sms(numbers, body):
    message = client.messages \
        .create(
            body=body,
            from_=DEFAULT_SENDER,
            to=numbers
        )

    print(message.body)
