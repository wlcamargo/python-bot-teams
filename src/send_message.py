import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
webhook_url = os.getenv("WEBHOOK_URL")

if not webhook_url:
    print("Error: WEBHOOK_URL is not defined in the environment variables.")
else:
    message = {
        "title": "Bot Message",
        "text": "Hello, this is an automated message sent to the Teams channel!"
    }
    response = requests.post(
        webhook_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(message)
    )
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(response.text)
