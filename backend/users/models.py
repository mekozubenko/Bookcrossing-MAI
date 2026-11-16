from django.contrib.auth.models import PermissionsMixin

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

from django.db import models

import hashlib
import secrets
from datetime import timedelta
from django.utils import timezone

class TelegramVerification(models.Model):

    class Status(models.TextChoices):
        PENDING = 'pending'
        VERIFIED = 'verified'

    token_hash = models.CharField(max_length=64, unique=True, db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    telegram_user_id = models.BigIntegerField(null=True, blank=True)
    telegram_username = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    verified_at = models.DateTimeField(null=True, blank=True)

    @classmethod
    def create_token(cls):
        """Генерирует одноразовый токен, сохраняет хеш, возвращает исходный токен"""
        raw_token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        obj = cls.objects.create(
            token_hash=token_hash,
            expires_at=timezone.now() + timedelta(minutes=15)
        )
        return raw_token, obj

    @classmethod
    def verify_token(cls, raw_token):
        """Проверяет токен, возвращает объект или None"""
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        try:
            obj = cls.objects.get(
                token_hash=token_hash,
                status=cls.Status.PENDING,
                expires_at__gt=timezone.now()
            )
            return obj
        except cls.DoesNotExist:
            return None


class UserManager(BaseUserManager):

    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError('Логин обязателен')

        user = self.model(
            login=login,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(login, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()

    class ContactType(models.TextChoices):
        PHONE_NUMBER = 'phone_number'
        TELEGRAM = 'telegram'

    class Status(models.TextChoices):
        PENDING = 'pending'
        VERIFIED = 'verified'

    login = models.CharField(max_length=255, unique=True, blank=False, null=False)
    contact_value = models.CharField(max_length=100, null=False, blank=False)
    contact_type = models.CharField(max_length=20, choices=ContactType.choices, default=ContactType.PHONE_NUMBER)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.login


