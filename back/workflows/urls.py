from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WorkflowViewSet, EtapeWorkflowViewSet,
    PatientWorkflowViewSet, EtapePatientViewSet
)

router = DefaultRouter()
router.register(r'workflows', WorkflowViewSet)
router.register(r'etapes', EtapeWorkflowViewSet)
router.register(r'patients', PatientWorkflowViewSet)
router.register(r'etapes-patient', EtapePatientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]