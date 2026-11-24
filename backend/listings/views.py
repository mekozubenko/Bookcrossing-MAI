from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status

from .serializers import ListingSerializer

from .models import Listing


class ListingViewSet(viewsets.ModelViewSet):

    #не знаю, нужен ли
    queryset = Listing.objects.all()

    serializer_class = ListingSerializer

    def get_queryset(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return Listing.objects.filter(user=self.request.user)

        return Listing.objects.all()
    #permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def get_my_listings(self, request):
        listings = Listing.objects.filter(user=request.user)
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'user/(?P<user_id>\d+)')
    def get_users_listings(self, request, user_id=None):
        listings = Listing.objects.filter(user_id=user_id)
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='contact')
    def get_contact(self, request, listing_id=None):
        listing = get_object_or_404(Listing, pk=listing_id)

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
