from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewset)

urlpatterns = [
    path('login/',LoginUser.as_view()),
    path('user/',GetUserView.as_view()),
    path('refresh/',RefreshTokenView.as_view()),
    path('', include(router.urls)),
]