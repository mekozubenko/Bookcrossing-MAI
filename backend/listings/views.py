from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings

from .models import Listing, TelegramVerification
from .serializers import ListingSerializer
from .sms import send_otp_sms

import logging
import time
import json
import requests

@csrf_exempt
def telegram_verification_start(request):

    raw_token, obj = TelegramVerification.create_token()
    bot_username = 'BookcrossingMAI_bot'
    bot_url = f"https://t.me/{bot_username}?start={raw_token}"

    return JsonResponse({
        'verification_id': obj.id,
        'bot_url': bot_url
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
    print(">>> BODY RAW:", request.body)
    if request.method != 'POST':
        return JsonResponse({'ok': False}, status=405)

    if not request.body:
        logger.warning("Telegram webhook received empty body")
        return JsonResponse({'ok': True})

    try:
        update = json.loads(request.body)
        message = update.get('message', {})
        text = message.get('text', '')

        logger.info("Update received: %s", update)

        if text.startswith('/start '):
            raw_token = text.split(' ', 1)[1].strip()
            verification = TelegramVerification.verify_token(raw_token)

            print(verification)

            if verification:
                from_user = message.get('from', {})
                verification.telegram_user_id = from_user.get('id')
                verification.telegram_username = from_user.get('username')
                verification.status = TelegramVerification.Status.VERIFIED
                verification.verified_at = timezone.now()

                # Переставить ниже и посмотреть чё произойдёт
                send_telegram_message(verification.telegram_user_id,"Telegram подтверждён! Вернитесь на сайт.")

                verification.save()

            else:
                pass
    except Exception:
        logger.exception("Telegram webhook processing failed")

    return JsonResponse({'ok': True})

@csrf_exempt
def telegram_verification_status(request, verification_id):
    try:
        obj = TelegramVerification.objects.get(id=verification_id)
        return JsonResponse({'status': obj.status})
    except TelegramVerification.DoesNotExist:
        return JsonResponse({'error': 'not found'}, status=404)

def submit_listing(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        phone = request.POST.get('phone', '').strip()

        if action == 'send_code':
            if not phone:
                messages.error(request, "Пожалуйста, введите номер телефона")
                return render(request, 'submit_form.html')

            # Перечекать!!!
            last_sent = request.session.get('otp_last_sent', 0)
            if time.time() - last_sent < 60:
                messages.error(request, "Слишком частая отправка, попробуйте позже")
                return render(request, 'submit_form.html', {'phone': phone})

            otp_code = send_otp_sms(phone)
            if otp_code:
                request.session['otp_code'] = otp_code
                request.session['otp_phone'] = phone
                request.session['otp_timestamp'] = time.time()
                request.session['otp_last_sent'] = time.time()
                messages.success(request, "Код подтверждения отправлен")
            else:
                messages.error(request, "Не удалось отправить, попробуйте позже")
            return render(request, 'submit_form.html', {'phone': phone})


        elif action == 'submit':
            user_code = request.POST.get('code', '').strip()
            saved_code = request.session.get('otp_code')
            saved_phone = request.session.get('otp_phone')
            saved_time = request.session.get('otp_timestamp', 0)

            # Перечекать!!!
            if phone != saved_phone:
                messages.error(request, "Номер телефона не совпадает")
            elif not saved_code or user_code != saved_code:
                messages.error(request, "Неверный код подтверждения")
            elif time.time() - saved_time > 300:
                messages.error(request, "Код истёк, запросите новый")
            else:

                Listing.objects.create(
                    title=request.POST.get('title'),
                    author=request.POST.get('author', 'Unknown'),
                    summary=request.POST.get('summary'),
                    contact_value=phone,
                    contact_type='phone_number',
                    location=request.POST.get('location', 'Unknown'),
                )

                for key in ['otp_code', 'otp_phone', 'otp_timestamp']:
                    request.session.pop(key, None)
                messages.success(request, "Заявка успешно отправлена!")
                return redirect('submit_listing')

    return render(request, 'submit_form.html')

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    #permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='contact')
    def get_contact(self, request, pk=None):
        listing = get_object_or_404(Listing, pk=pk)

        return Response({
            'listing_id': listing.id,
            'contact_value': listing.contact_value,
        })

    @action(detail=True, methods=['get'], url_path='location')
    def get_location(self, request, pk=None):
        listing = get_object_or_404(Listing, pk=pk)

        return Response({
            'listing_id': listing.id,
            'location': listing.location,
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        listing = serializer.save()
        return Response(
            {"id": listing.id},
            status=status.HTTP_201_CREATED
        )



# Create your views here.
