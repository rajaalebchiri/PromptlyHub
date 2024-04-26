"""Tasks for queue"""
import os
import requests

from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN")
API_KEY = os.getenv("MAILGUN_API_KEY")

def send_simple_message(to, subject, body):
    """Send a simple email"""
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", API_KEY),
        data={
            "from": f"PromptlyHub <mailgun@{DOMAIN}>",
            "to": [to],
            "subject": subject,
            "text": body
        }
    )

def send_user_registration_email(email, username):
    return send_simple_message(
        email,
        "Successfully registered",
        f"Hi {username}! You have successfully signed up to PromptlyHub REST API"
    )