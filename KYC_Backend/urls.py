from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('registration_API.urls')),
    path('api/', include('login_API.urls')),
    path('otp/', include('otp_API.urls')),
    path("api/licenses/", include("licenses_API.urls")),
]
