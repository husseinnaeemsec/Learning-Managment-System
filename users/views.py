from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer
import logging

auth_logger = logging.getLogger('app_login')
registration_logger = logging.getLogger('app_register')
logout_logger = logging.getLogger('app_logout')


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            registration_logger.info(f"User {user.username} registered successfully.")
            return Response({"message": "User created successfully"}, status=HTTP_201_CREATED)
        registration_logger.warning(f"Registration failed: {serializer.errors}")
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)



class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Validate the incoming data with the LoginSerializer
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data # Get the user object after validation

            # Create JWT tokens (access and refresh)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)  # Get the access token

            # Log the successful login
            auth_logger.info(f"User {user.username} logged in.")

            # Return the access token and token class (JWT)
            return Response({
                "access_token": access_token,
                "token_class": "JWT"
            }, status=HTTP_200_OK)
        
        # If login failed, log the error and return the validation errors
        auth_logger.warning(f"Login failed: {serializer.errors}")
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data
            token.delete()
            auth_logger.info(f"User {request.user.username} logged out.")
            return Response({"message": "Logged out successfully"}, status=HTTP_200_OK)
        auth_logger.warning(f"Logout failed: {serializer.errors}")
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# Check authentication

