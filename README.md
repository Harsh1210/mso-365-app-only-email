# 📧 App-Only Email Sender (Microsoft Graph + AWS Secrets Manager)

## 📝 Description

This Python script enables sending emails from an Azure-registered app using **Microsoft Graph API with app-only authentication**, making it ideal for background tasks, automations, or internal tools. It integrates with **AWS Secrets Manager** to securely manage credentials (`CLIENT_ID`, `CLIENT_SECRET`, `TENANT_ID`, `ALLOWED_SENDERS`), and reads the sender and recipient emails from a simple `.env` file.

The script ensures that only **approved sender addresses** (as defined in AWS) can send mail, and supports sending to multiple recipients. It's designed for cloud-native environments, such as **cron jobs, Docker containers, EC2**, or **Lambda functions**.

---

## 📁 Folder Structure
project-root/
├── email_sender.py
├── .env
├── .gitignore
└── README.md
---

## 🧪 Prerequisites

- Python 3.7+
- AWS CLI configured with credentials or IAM role access
- Microsoft 365 tenant + Azure App Registration with admin consent

---

## 🔐 AWS Secrets Manager Setup

1. Go to AWS Secrets Manager → Create a secret named `AppOnlyEmailer`
2. Choose region: `ap-south-1`
3. Store secret as JSON:

```json
{
  "CLIENT_ID": "your-client-id",
  "CLIENT_SECRET": "your-client-secret",
  "TENANT_ID": "your-tenant-id",
  "ALLOWED_SENDERS": "support@lumiq.ai,alerts@lumiq.ai"
}
```
---
## 📄 .env File

Create a .env file in the project root with just:
 ```bash
 # .env
SENDER_EMAIL=support@abc.com
RECEIVER_EMAIL=harsh.agarwal@abc.com,alerts@abc.com
```
---
## 🛠 Installation

Install required Python packages:
```bash
pip install requests python-dotenv boto3
OUTPUT:
✅ Email sent successfully.
```
---
## 🛡 Behavior Summary
	•	✅ Fetches credentials from AWS Secrets Manager (AppOnlyEmailer)
	•	✅ Reads sender & receiver email addresses from .env
	•	✅ Validates that SENDER_EMAIL is in ALLOWED_SENDERS
	•	✅ Sends mail using Microsoft Graph /sendMail endpoint
	•	✅ Supports multiple recipients

---

## 📬 Example Email
	•	From: support@abc.com
	•	To: harsh.agarwal@abc.com,alerts@abc.com
	•	Subject: 🚀 AWS Secrets + App-only Email Test
	•	Body:
Hello,

This email was sent using Microsoft Graph API with AWS Secrets Manager integration.

Regards,
Team

## 📎 References
	•	Microsoft Graph API - Send Mail
	•	Microsoft Identity Platform - Client Credentials Flow
	•	AWS Secrets Manager (boto3)
