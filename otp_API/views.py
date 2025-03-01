import random
from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from otp_API.db_mongo import get_otp_collection

class SendOTP(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a 6-digit OTP
        otp = str(random.randint(100000, 999999))
        otp_collection = get_otp_collection()

        # Save or update the OTP in the database
        otp_collection.update_one(
            {"email": email},
            {"$set": {
                "otp": otp,
                "created_at": datetime.utcnow()
            }},
            upsert=True
        )

        # Render the email template
        email_body = render_to_string('otp_email_template.html', {'otp': otp})

        # Send the email
        email_message = EmailMessage(
            subject='Your OTP for Registration - Pratyaksha',
            body=email_body,
            from_email='shri2sontakke@gmail.com',  # Replace with your email
            to=[email],
        )
        email_message.content_subtype = 'html'  # Set the email content type to HTML
        email_message.send()

        return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)


class VerifyOTP(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({"error": "Email and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

        otp_collection = get_otp_collection()
        otp_entry = otp_collection.find_one({"email": email})

        if not otp_entry:
            return Response({"error": "No OTP found for this email"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the OTP is valid and not expired
        created_at = otp_entry["created_at"]
        if otp_entry["otp"] == otp and datetime.utcnow() - created_at <= timedelta(minutes=5):
            return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
        elif datetime.utcnow() - created_at > timedelta(minutes=5):
            return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
