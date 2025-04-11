from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlerteCritereViewSet, NotificationViewSet, ReglageNotificationViewSet

router = DefaultRouter()
router.register(r'criteres', AlerteCritereViewSet)
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'reglages', ReglageNotificationViewSet, basename='reglage')

urlpatterns = [
    path('', include(router.urls)),
]