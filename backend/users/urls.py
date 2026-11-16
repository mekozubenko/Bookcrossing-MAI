from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet, basename='users')


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/telegram/start/', views.telegram_verification_start, name='tg_start'),
    path('api/telegram/webhook/', views.telegram_webhook, name='tg_webhook'),
    path('api/telegram/verification/<int:verification_id>/', views.telegram_verification_status, name='tg_status'),
    path('api/check/', views.check_phone, name='check_phone'),
]