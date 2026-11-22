import requests
from django.conf import settings

def get_jwt_token():
    url = "http://one-api.notificore.ru/api/auth/login"

    response = requests.post(
        url, json={"api_key": settings.NOTIFICORE_API_KEY}, timeout=10
    )

    response.raise_for_status()

    return response.json()["bearer"]


def send_otp_sms(phone_number):

    jwt_token = get_jwt_token()

    url = "https://one-api.notificore.ru/api/2fa/authentications/otp"

    payload = {
        "channel": "sms",
        "recipient": phone_number.lstrip('+'),
        "sender": settings.NOTIFICORE_SENDER,
        "template_id": settings.NOTIFICORE_TEMPLATE_ID,
        "code_digits": 5,
        "code_max_tries": 3,
        "code_lifetime": 300
    }

    print(payload)

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

    print(headers)

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=(5, 30)
    )

    print("Status code:", response.status_code)
    print("Response body:", response.text)

    response.raise_for_status()
    data = response.json()

    print(data)

    return data["data"]["id"]

def verify_otp_sms(id, access_code):

    jwt_token = get_jwt_token()

    url = f"https://one-api.notificore.ru/api/2fa/authentications/otp/{id}/verify"

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json={"access_code": access_code}, headers=headers, timeout=(5, 30))

    print("Status:", response.status_code)
    print("Response:", response.text)

    response.raise_for_status()
    data = response.json()

    return data["data"]["status"]