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

    title = models.CharField(max_length=200)
    summary = models.TextField()
    contact_value = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    consent_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title


# Create your models here.
