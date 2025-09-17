from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_405_METHOD_NOT_ALLOWED, HTTP_201_CREATED
import json
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework import status
from donations.models import Donation
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from django.conf import settings

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Logs in the user."""
    data = request.data
    email = data.get("email")
    password = data.get("password")
    user = authenticate(request, email=email, password=password)

    print(user)
    if user is not None:
        login(request, user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        print("access token: "+ access_token)
        return JsonResponse({"message": "Login successful",'access_token': access_token,'refresh_token': str(refresh)}, status=HTTP_200_OK)
    return JsonResponse({"error": "Invalid credentials"}, status=HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout_user(request):
    """Logs out the user and blacklists the refresh token."""
    try:
        # Extract the refresh token from the request
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({"error": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Parse the refresh token
        token = RefreshToken(refresh_token)
        jti = token['jti']

        # Check if the token is already blacklisted
        if BlacklistedToken.objects.filter(token__jti=jti).exists():
            return Response({"error": "Token is already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the corresponding outstanding token
        outstanding_token = OutstandingToken.objects.get(jti=jti)

        # Blacklist the token
        BlacklistedToken.objects.create(token=outstanding_token)

        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    except OutstandingToken.DoesNotExist:
        return Response({"error": "Token not found in OutstandingToken"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "Failed to logout", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_user(request):
    """Edits the profile of the logged-in user."""
    user = request.user
    data = request.data
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    if data.get("password"):
        user.password = make_password(data.get("password"))
    user.save()
    return Response({"message": "Profile updated successfully"}, status=HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    """Registers a new user and generates JWT tokens."""
    data = request.data
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return Response({"error": "All fields are required"}, status=HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already exists"}, status=HTTP_400_BAD_REQUEST)

    try:
        # Create the user
        user = User.objects.create(
            name=name,  # Using `username` as Django's default User model doesn't have a `name` field
            email=email,
            password=make_password(password)
        )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User created successfully",
                "user_id": user.id,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            },
            status=HTTP_201_CREATED,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)

from datetime import datetime

@api_view(['GET'])
def view_user(request):
    """Returns a detailed view of the profile of the logged-in user."""
    if request.method == "GET":
        print(f"Authorization Header: {request.headers.get('Authorization')}")
        user = request.user
        
        # total donations done by the user:
        all_donations = Donation.objects.filter(user_id=user.id)
        donated_amount = sum(donation.amount for donation in all_donations)

        # Check if last_login is None, and if so, set it to the current time
        last_login = user.last_login.date() if user.last_login else datetime.now().date()

        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "date_joined": user.date_joined.date(),
            "last_login": last_login,
            "donated_amount": donated_amount
        }
        return JsonResponse(user_data, status=200)
    
    # Handle other methods (like POST) if needed
    return JsonResponse({"error": "Only GET requests are allowed for this endpoint."}, status=405)


from datetime import datetime
from django.db.models import Q

# Clean expired tokens in OutstandingToken
def clean_expired_tokens():
    now = datetime.now()
    expired_tokens = OutstandingToken.objects.filter(expires_at__lt=now)
    expired_tokens.delete()

