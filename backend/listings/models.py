from django.db import models
from django.utils import timezone
import uuid

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
