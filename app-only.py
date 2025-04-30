import os
import json
import boto3
import requests
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# === Load .env values ===
load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAILS = os.getenv("RECEIVER_EMAIL", "").split(",")

# === Fetch credentials from AWS Secrets Manager ===
def get_secrets():
    secret_name = "AppOnlyEmailer"
    region_name = "ap-south-1"
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    except ClientError as e:
        raise RuntimeError(f"Failed to retrieve secrets: {e}")

secrets = get_secrets()

CLIENT_ID = secrets["CLIENT_ID"]
CLIENT_SECRET = secrets["CLIENT_SECRET"]
TENANT_ID = secrets["TENANT_ID"]
ALLOWED_SENDERS = [email.strip() for email in secrets["ALLOWED_SENDERS"].split(",")]

# === Validate Sender ===
if SENDER_EMAIL not in ALLOWED_SENDERS:
    raise ValueError(f"❌ Sender '{SENDER_EMAIL}' is not in allowed list.")

# === Get App Token ===
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

# === Send Email ===
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Build recipients list
recipients = [{"emailAddress": {"address": addr.strip()}} for addr in RECEIVER_EMAILS]

email_payload = {
    "message": {
        "subject": "🚀 AWS Secrets + App-only Email Test",
        "body": {
            "contentType": "Text",
            "content": "Hello,\n\nThis email was sent using Microsoft Graph API with AWS Secrets Manager integration.\n\nRegards,\nLumiq Team"
        },
        "toRecipients": recipients
    },
    "saveToSentItems": "false"
}

send_url = f"https://graph.microsoft.com/v1.0/users/{SENDER_EMAIL}/sendMail"
response = requests.post(send_url, headers=headers, json=email_payload)

# === Result ===
if response.status_code == 202:
    print("✅ Email sent successfully.")
else:
    print(f"❌ Failed to send email: {response.status_code}")
    print(response.text)