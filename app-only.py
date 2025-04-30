import os
import requests
from dotenv import load_dotenv

# Load from .env
load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
ALLOWED_SENDERS = os.getenv("ALLOWED_SENDERS", "").split(",")

if SENDER_EMAIL not in ALLOWED_SENDERS:
    raise ValueError(f"❌ Sender email '{SENDER_EMAIL}' is not allowed.")

# Step 1: Get App Token
token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
token_data = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'scope': 'https://graph.microsoft.com/.default'
}

token_response = requests.post(token_url, data=token_data)
token_response.raise_for_status()
access_token = token_response.json()['access_token']

# Step 2: Send Email
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

email_payload = {
    "message": {
        "subject": "✅ App-only Email Test",
        "body": {
            "contentType": "Text",
            "content": "Hi Harsh,\n\nThis is an automated test email sent using app-only authentication.\n\n- Lumiq Bot"
        },
        "toRecipients": [
            {"emailAddress": {"address": "harsh.agarwal@lumiq.ai"}}
        ]
    },
    "saveToSentItems": "false"
}

# Note: /users/{email}/sendMail allows app to impersonate the sender
graph_url = f"https://graph.microsoft.com/v1.0/users/{SENDER_EMAIL}/sendMail"
response = requests.post(graph_url, headers=headers, json=email_payload)

if response.status_code == 202:
    print("✅ Email sent successfully!")
else:
    print(f"❌ Email failed: {response.status_code}")
    print(response.text)