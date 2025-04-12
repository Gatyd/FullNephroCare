from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny

class PublicSwaggerView(SpectacularSwaggerView):
    permission_classes = [AllowAny]

# admin.site.login = login_required(admin.site.login)

urlpatterns = [

    # API DOCUMENTATION
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    path('',include('authentication.urls')),
    path('',include('patients.urls')),
    path('',include('consultations.urls')),
    path('',include('notifications.urls')),
    path('',include('workflows.urls')),
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]