from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'traitements', TraitementViewSet)
router.register(r'resultats-examens', ResultatExamenViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
