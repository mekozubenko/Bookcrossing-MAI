import hashlib
import secrets
from django.db import models
from django.utils import timezone
from datetime import timedelta

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

class Listing(models.Model):

    class Status(models.TextChoices):
        PENDING = 'pending'
        ACTIVE = 'active'
        GIVEN = 'given'
        HIDDEN = 'hidden'
        ARCHIVED = 'archived'

    class Genre(models.TextChoices):
        CLASSIC = 'classic'
        FANTASY = 'fantasy'
        FICTION = 'fiction'
        LOVE = 'love'
        DETECTIVE = 'detective'
        THRILLER = 'thriller'
        BIOGRAPHY = 'biography'
        JOURNALISM = 'journalism'
        HISTORICAL = 'historical'
        HORROR = 'horror'
        ADVENTURES = 'adventures'
        POETRY = 'poetry'
        FOLKLORE = 'folklore'
        HUMOR = 'humor'
        PSYCHOLOGY = 'psychology'
        BUSINESS = 'business'
        COMICS = 'comics'
        MANGA = 'manga'
        PROFESSIONAL = 'professional'
        SCIENCE = 'science'
        INARTISTIC = 'inartistic'
        OTHER = 'other'
        UNKNOWN = 'unknown'

    class ContactType(models.TextChoices):
        PHONE_NUMBER = 'phone_number'
        TELEGRAM = 'telegram'

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, default='Unknown')
    genre = models.CharField(max_length=200, choices=Genre.choices, default=Genre.UNKNOWN)
    summary = models.TextField()
    contact_value = models.CharField(max_length=100, default='Unknown')
    contact_type = models.CharField(max_length=20, choices=ContactType.choices, default=ContactType.PHONE_NUMBER)
    photo_url = models.URLField(null=True, blank=True)
    location = models.CharField(max_length=200, default='Unknown')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    consent_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title
