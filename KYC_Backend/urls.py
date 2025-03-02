from django.contrib import admin
from django.urls import path, include
from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('api/', include('registration_API.urls')),
    path('api/', include('login_API.urls')),
    path('otp/', include('otp_API.urls')),
    path("api/licenses/", include("licenses_API.urls")),
]
