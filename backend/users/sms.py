import requests
from django.conf import settings


def send_otp_sms(phone_number):
    url = "https://api.notificore.ru/rest/sms/create"

    payload = {
        "destination": "phone",
        "originator": settings.NOTIFICORE_SENDER,
        "body": "Ваш код подтверждения: {gen_otp_09,4}",
        "msisdn": phone_number.lstrip('+'),
    }

    headers = {
        "X-API-KEY": settings.NOTIFICORE_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("error") == "0":
            return data.get("otp_code") or data.get("result", {}).get("otp_code")
        else:
            return None
    except requests.exceptions.RequestException:
        return None