from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'listings', views.ListingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path("api/listings/", include("rest_framework.urls")),
    path('api/listings/<int:listing_id>/', include("rest_framework.urls")),
    path('submit/', views.submit_listing, name='submit_listing'),
    path('api/telegram/start/', views.telegram_verification_start, name='tg_start'),
    path('api/telegram/webhook/', views.telegram_webhook, name='tg_webhook'),
    path('api/telegram/verification/<int:verification_id>/',
         views.telegram_verification_status, name='tg_status'),
]