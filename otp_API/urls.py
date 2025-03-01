from django.urls import path
from otp_API.views import SendOTP, VerifyOTP

urlpatterns = [
    path('send-otp/', SendOTP.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTP.as_view(), name='verify-otp'),
]
