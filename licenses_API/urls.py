from django.urls import path
from .views import PurchaseLicenseView, AssignLicenseView, LicenseStatusView

urlpatterns = [
    path('purchase/', PurchaseLicenseView.as_view(), name='purchase_license'),
    path('assign/', AssignLicenseView.as_view(), name='assign_license'),
    path('status/<str:license_id>/', LicenseStatusView.as_view(), name='license_status'),
]
