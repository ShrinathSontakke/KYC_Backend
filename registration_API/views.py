from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .db_mongo import users_collection
from datetime import datetime
from .utils import validate_email_format, validate_password_strength


class RegisterView(APIView):
    def post(self, request):
        data = request.data

        # Check if all required fields are present
        required_fields = [
            "firstName",
            "lastName",
            "dob",
            "gender",
            "email",
            "phoneNumber",
            "streetAddress",
            "city",
            "state",
            "postalCode",
            "country",
            "password",
            "confirmPassword",
        ]

        for field in required_fields:
            if field not in data or not data[field]:
                return Response(
                    {"error": f"{field} is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Validate email format
        if not validate_email_format(data["email"]):
            return Response(
                {"error": "Invalid email format."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate password strength
        is_strong, password_message = validate_password_strength(data["password"])
        if not is_strong:
            return Response(
                {"error": password_message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Set default role to "initiator" if not provided
        valid_roles = {"initiator", "recipient", "admin"}
        data["role"] = data.get("role", "initiator").lower()

        if data["role"] not in valid_roles:
            return Response(
                {"error": "Invalid role. Allowed roles: initiator, recipient, admin."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Check for duplicate email or phone number
            existing_user = users_collection.find_one(
                {"$or": [{"email": data["email"]}, {"phoneNumber": data["phoneNumber"]}]}
            )
            if existing_user:
                return Response(
                    {"error": "Email or phone number already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Hash the password before saving
            data["password"] = make_password(data["password"])

            # Add created_at and updated_at timestamps
            data["created_at"] = datetime.utcnow()
            data["updated_at"] = datetime.utcnow()

            # Insert the data into MongoDB
            users_collection.insert_one(data)

            return Response(
                {
                    "message": "Registration successful!",
                    "user": {
                        "firstName": data["firstName"],
                        "lastName": data["lastName"],
                        "email": data["email"],
                        "phoneNumber": data["phoneNumber"],
                        "role": data["role"],
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
