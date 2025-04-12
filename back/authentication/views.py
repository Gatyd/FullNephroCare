from rest_framework.views import APIView, exception_handler
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now
from .serializers import LoginSerializer, UserSerializer
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from authentication.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, (InvalidToken, TokenError, AuthenticationFailed, NotAuthenticated)):
        return Response(
            {
                "detail": str(exc),
                "code": "token_not_valid"
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    return response

class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if hasattr(view, 'action') and view.action == 'list':
            return request.user and request.user.is_superuser
        if hasattr(view, 'action') and view.action == 'create':
            return request.user and request.user.is_superuser
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return True if request.user.is_superuser else obj.id == request.user.id


class LoginUser(APIView):
    permission_classes = []
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            user.last_login = now()
            user.save()
            reponse = Response(UserSerializer(user).data, status=status.HTTP_200_OK)
            reponse.set_cookie(
                'access_token',
                str(refresh.access_token),
                max_age=3600 * 2, # 2 hour
                httponly=True,
                secure=True if settings.DEBUG == False else False,
                samesite='Lax'
            )
            reponse.set_cookie(
                'refresh_token',
                str(refresh),
                max_age=7*24*3600, # 1 week
                httponly=True,
                secure=True if settings.DEBUG == False else False,
                samesite='Lax'
            )
            return reponse
        return Response({"Connexion impossible": "Identifiants invalides"}, status=status.HTTP_400_BAD_REQUEST)
    
class GetUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            print("Access token non fourni.")
            raise AuthenticationFailed('Access token non fourni.')

        try:
            user = request.user
            return Response(UserSerializer(user).data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]

    # def get_permissions(self):
    #     if self.action in ['create', 'update', 'partial_update']:
    #         return [AllowAny()]
    #     return super().get_permissions()

    # def perform_create(self, serializer):
    #     serializer.save()

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            print("Refresh token non fourni.")
            raise AuthenticationFailed('Refresh token non fourni.')

        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            user = User.objects.get(id=token["user_id"])

        except TokenError:
            raise AuthenticationFailed('Token invalide ou expiré.')

        response = Response(UserSerializer(user).data, status=status.HTTP_200_OK)

        response.set_cookie(
            key='access_token',
            value=access_token,
            max_age=3600 * 2, # 2 hour
            httponly=True,
            secure=True if settings.DEBUG == False else False,
            samesite='Lax'
        )

        return response
    
class LogoutUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response(status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response