import requests
import json
import os

def send_message_to_slack(message):
    webhook_url = os.getenv('SLACK_CONNECT')

    if not webhook_url:
        print("Error: Slack webhook URL not found in environment variables.")
        return

    payload = {
        "text": message
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Send the message to Slack using a POST request
        requests.post(webhook_url, data=json.dumps(payload), headers=headers)

    except Exception as e:
        print("Error sending the message:", str(e))