import jwt
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.conf import settings
from .db_mongo import collection


class LoginView(APIView):
    def post(self, request):
        data = request.data

        # Validate input
        if "email" not in data and "phoneNumber" not in data:
            return Response(
                {"error": "Email or phone number is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if "password" not in data or not data["password"]:
            return Response(
                {"error": "Password is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Find user by email or phone number (case-insensitive for email)
            user = collection.find_one({
                "$or": [
                    {"email": {"$regex": f"^{data.get('email')}$", "$options": "i"}},
                    {"phoneNumber": data.get("phoneNumber")}
                ]
            })

            if not user:
                return Response(
                    {"error": "User not found. Please check your email or phone number."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Check password
            if not check_password(data["password"], user["password"]):
                return Response(
                    {"error": "Invalid password."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Generate JWT tokens
            access_token_payload = {
                "user_id": str(user["_id"]),  # MongoDB's `_id` is typically ObjectId
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),  # Token expires in 30 minutes
                "iat": datetime.datetime.utcnow(),
            }
            refresh_token_payload = {
                "user_id": str(user["_id"]),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),  # Refresh token expires in 1 day
                "iat": datetime.datetime.utcnow(),
            }

            access_token = jwt.encode(
                access_token_payload, settings.SECRET_KEY, algorithm="HS256"
            )
            refresh_token = jwt.encode(
                refresh_token_payload, settings.SECRET_KEY, algorithm="HS256"
            )

            return Response(
                {
                    "message": "Login successful!",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "firstName": user["firstName"],
                        "lastName": user["lastName"],
                        "email": user["email"],
                        "phoneNumber": user["phoneNumber"],
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
