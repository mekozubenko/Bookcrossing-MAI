from rest_framework import viewsets

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings

from .models import User, TelegramVerification
from .serializers import UserRegisterSerializer, UserGetSerializer

from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action
from rest_framework import status

from datetime import timedelta

from .sms import send_otp_sms, verify_otp_sms

import logging
import time
import json
import requests

def cleanup_unverified_users():
    deadline = timezone.now() - timedelta(hours=24)

    User.objects.filter(
        status=User.Status.PENDING,
        created_at__lt=deadline
    ).delete()

@csrf_exempt
def telegram_verification_start(request, user):

    raw_token, obj = TelegramVerification.create_token(user)

    bot_username = 'BookcrossingMAI_bot'
    bot_url = f'https://t.me/{bot_username}?start={raw_token}'

    return JsonResponse({
        'success': True,
        'message': 'Подтвердите аккаунт через Telegram',
        'verification_type': 'telegram',
        'verification_id': obj.id,
        'bot_url': bot_url,
    })


logger = logging.getLogger(__name__)

@csrf_exempt
def send_telegram_message(chat_id, text):
    """Вспомогательная функция: отправка сообщения через Bot API"""
    bot_token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    print("Token:", bot_token)
    try:
        requests.post(url, json={'chat_id': chat_id, 'text': text}, timeout=5)
        logger.info("body=%s", text)
    except requests.exceptions.RequestException:
        logger.exception("Failed to send Telegram message")


@csrf_exempt
def telegram_webhook(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False}, status=405)

    if not request.body:
        return JsonResponse({'ok': True})

    try:
        update = json.loads(request.body)
        message = update.get('message', {})
        text = message.get('text', '')

        if not text.startswith('/start '):
            return JsonResponse({'ok': True})

        raw_token = text.split(' ', 1)[1].strip()

        verification = TelegramVerification.verify_token(raw_token)

        if not verification or not verification.user:
            return JsonResponse({'ok': True})

        from_user = message.get('from', {})
        telegram_user_id = from_user.get('id')

        if not telegram_user_id:
            return JsonResponse({'ok': True})

        verification.telegram_user_id = telegram_user_id
        verification.telegram_username = from_user.get('username')
        verification.status = TelegramVerification.Status.VERIFIED
        verification.verified_at = timezone.now()
        verification.save()

        user = verification.user
        user.status = User.Status.VERIFIED
        user.save(update_fields=['status'])

        send_telegram_message(
            telegram_user_id,
            'Telegram подтверждён! Ваш аккаунт успешно зарегистрирован. Вернитесь на сайт.'
        )

    except Exception:
        logger.exception('Telegram webhook processing failed')

    return JsonResponse({'ok': True})

@csrf_exempt
def telegram_verification_status(request, verification_id):
    try:
        obj = TelegramVerification.objects.get(id=verification_id)
        return JsonResponse({'status': obj.status})
    except TelegramVerification.DoesNotExist:
        return JsonResponse({'error': 'not found'}, status=404)

def start_check_phone(request, user):
    phone = user.contact_value

    verification_id = send_otp_sms(phone)

    if not verification_id:
        return JsonResponse({
            'status': False,
            'error': 'Не удалось отправить SMS'
        }, status=400)

    request.session['verification_id'] = verification_id
    request.session['otp_phone'] = phone
    request.session['otp_timestamp'] = time.time()
    request.session['otp_last_sent'] = time.time()

    return JsonResponse({
        'status': True,
        'message': 'Код подтверждения отправлен',
        'verification_type': 'phone',
        'contact_value': phone,
        'user': user.id,
        'verification_id': verification_id
    })

class RegisterView(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):

        cleanup_unverified_users()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        if user.contact_type == User.ContactType.PHONE_NUMBER:

            result = start_check_phone(request, user)

            return result

        elif user.contact_type == User.ContactType.TELEGRAM:

            result = telegram_verification_start(request, user)

            return result

        return JsonResponse(
            {'error': 'Неизвестный тип контакта'},
            status=status.HTTP_400_BAD_REQUEST
        )



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserGetSerializer

    @action(detail=False, methods=['post'], url_path='verify-phone')
    def verify_phone(self, request):
        user_id = request.data.get('user')
        user = User.objects.get(id=user_id)
        print(user, user.status)
        verification_id = request.data.get('verification_id')
        code = request.data.get('code')

        if not verification_id or not code:
            return JsonResponse(
                {'error': 'Необходимо передать ID проверки и код'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = verify_otp_sms(verification_id, code)

        print(result)

        if result == 'verified':
            user.status = User.Status.VERIFIED
            user.save(update_fields=['status'])
            return JsonResponse(
                {'verified': True, 'message': 'Телефон подтверждён'},
                status=status.HTTP_200_OK
            )

        return JsonResponse(
            {'verified': False, 'message': 'Неверный код'},
            status=status.HTTP_400_BAD_REQUEST
        )

# Create your views here.
