from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Listing
        fields = ['id', 'title', 'summary', 'contact_value', 'status', 'consent_at', 'created_at']