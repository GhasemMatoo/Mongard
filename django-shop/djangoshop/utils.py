import requests
import json


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
        'X-API-KEY': 'tRZLQOg4qXH9enU6Thi2AAAwWFUF5K32b3UX0PpLxu9DOH0RbIQCsNyItYwtWDTC'
    }
    request = requests.post("https://api.sms.ir/v1/send/verify", data=data, headers=headers)
    return request.status_code == 200
