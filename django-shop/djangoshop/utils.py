import requests
import json
import environ
from django.conf import settings

env = environ.Env()
env.read_env(str(settings.BASE_DIR / ".sms_env"))


def send_otp_code(phone_number, otp_code):
    data = json.dumps({
        "mobile": phone_number,
        "templateId": 100000,
        "parameters": [
            {
                "name": "Code",
                "value": otp_code
            }
        ]})
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'text/plain',
        'X-API-KEY': env("X_API_KEY")
    }
    request = requests.post("https://api.sms.ir/v1/send/verify", data=data, headers=headers)
    return request.status_code == 200
