from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Listing
        fields = ['id', 'title', 'genre', 'author', 'summary', 'photo_url', 'location', 'contact_value', 'contact_type', 'consent_at', 'created_at']