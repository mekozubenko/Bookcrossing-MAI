from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status

from .models import Listing
from .serializers import ListingSerializer

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        listing = serializer.save()
        return Response(
            {"id": listing.id},
            status=status.HTTP_201_CREATED
        )



# Create your views here.
