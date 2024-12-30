from django.contrib.auth import get_user_model
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from rest_framework import generics
from .serializers import UserSerializer, AdminRegistrationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsAdmin, IsHR, IsFinance

CustomUser = get_user_model()

class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class AdminRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AdminRegistrationSerializer
    permission_classes = [IsAuthenticated]  # Restrict to authenticated users

@method_decorator(
    ratelimit(key="ip", rate="5/m", method="POST", block=True),
    name="dispatch"
)
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            data = response.data

            if "access" in data and "refresh" in data:
                # Set access_token
                response.set_cookie(
                    "access_token",
                    data["access"],
                    httponly=True,
                    secure=False,  # Set to True in production
                    samesite="None",  # Required for cross-origin requests
                )

                # Set refresh_token
                response.set_cookie(
                    "refresh_token",
                    data["refresh"],
                    httponly=True,
                    secure=False,  # Set to True in production
                    samesite="None",
                )

                # Remove tokens from response body
                response.data.pop("access", None)
                response.data.pop("refresh", None)

            return response
        except Exception as e:
            print(f"Error during token generation: {str(e)}")
            return Response({"detail": "Internal server error."}, status=500)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView

class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"detail": "Refresh token missing."}, status=401)

        try:
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)
            response = Response({"access_token": new_access_token})
            response.set_cookie(
                "access_token",
                new_access_token,
                httponly=True,
                secure=False,  # Set True in production
                samesite="None",  # Adjust based on your frontend setup
            )
            return response
        except Exception as e:
            print(f"Refresh token validation error: {e}")
            return Response({"detail": "Invalid refresh token."}, status=401)

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response({"detail": "Logged out successfully"})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

# Add the CheckAuthView here
class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "is_authenticated": True,
            "user": request.user.username,
            "role": getattr(request.user, "role", "employee"),
        })


class AdminDashboardView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({"message": "Welcome to the Admin Dashboard"})

class HRDashboardView(APIView):
    permission_classes = [IsHR]

    def get(self, request):
        return Response({"message": "Welcome to the HR Dashboard"})
    
class FinanceDashboardView(APIView):
    permission_classes = [IsFinance]

    def get(self, request):
        return Response({"message": "Welcome to the Finance Dashboard"})