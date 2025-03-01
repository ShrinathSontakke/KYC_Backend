import uuid
from bson import ObjectId
from datetime import datetime
from rest_framework import status
from .services import send_purchase_email , send_license_assignment_email
from rest_framework.views import APIView
from rest_framework.response import Response
from dateutil.relativedelta import relativedelta
from .db_mongo import licenses_collection, license_assignments_collection
from registration_API.db_mongo import users_collection
from .serializers import LicenseSerializer, LicenseAssignmentSerializer

# Mapping license types to their validity in months
LICENSE_VALIDITY = {
    "Basic": 3,       # 3 months
    "Premium": 6,     # 6 months
    "Enterprise": 12  # 12 months
}

class PurchaseLicenseView(APIView):
    def post(self, request):
        data = request.data

        # Validate input (excluding validity_period)
        serializer = LicenseSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Validate initiator_id
        initiator = users_collection.find_one({"_id": ObjectId(data["initiator_id"])})
        if not initiator:
            return Response({"error": "Register before purchasing the license"}, status=status.HTTP_400_BAD_REQUEST)

        initiator_email = initiator["email"]

        # Check if user already has a license
        existing_license = licenses_collection.find_one({"initiator_id": data["initiator_id"]})
        if existing_license:
            return Response({"error": "You have already purchased a license. Only one license is allowed per user."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate license type
        license_type = data.get("license_type")
        if license_type not in LICENSE_VALIDITY:
            return Response({"error": "Invalid license type"}, status=status.HTTP_400_BAD_REQUEST)

        validity_months = LICENSE_VALIDITY[license_type]

        # Calculate purchase_date and valid_until
        purchase_date = datetime.utcnow()
        valid_until = purchase_date + relativedelta(months=validity_months)

        # Generate unique license_id
        license_id = str(ObjectId())

        # Prepare license data
        license_data = {
            "_id": license_id,
            "initiator_id": data["initiator_id"],
            "license_id": license_id,
            "initiator_email": initiator_email,
            "license_type": license_type,
            "validity_period": f"{validity_months * 30} days",  # Stores as "90 days", "180 days".
            "total_slots": data["total_slots"],
            "used_slots": 0,
            "purchase_date": purchase_date,
            "valid_until": valid_until,
            "status": "active"
        }

        # Insert into MongoDB
        licenses_collection.insert_one(license_data)

        # Send email notification
        send_purchase_email(initiator_email, data["license_type"], license_data["validity_period"])

        return Response({
            "message": "License purchased successfully!",
            "license_id": license_id,
            "valid_until": valid_until.strftime("%Y-%m-%d")
        }, status=status.HTTP_201_CREATED)

# Assign License to Recipients
class AssignLicenseView(APIView):
    def post(self, request):
        data = request.data

        # Validate input
        serializer = LicenseAssignmentSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Find license by ID
        license_entry = licenses_collection.find_one({"_id": data["license_id"]})
        if not license_entry:
            return Response({"error": "License not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the recipient_email is already assigned to this license
        existing_assignment = license_assignments_collection.find_one({
            "license_id": data["license_id"],
            "recipient_email": data["recipient_email"]
        })
        if existing_assignment:
            return Response({"error": "This KYC has already been assigned to this Person"}, status=status.HTTP_400_BAD_REQUEST)

        # Check available slots
        if license_entry["used_slots"] >= license_entry["total_slots"]:
            return Response({"error": "No available slots in this license"}, status=status.HTTP_400_BAD_REQUEST)
        
         # Extract and validate type_of_KYC and types_of_Documents
        type_of_KYC = data.get("type_of_KYC", [])
        types_of_Documents = data.get("types_of_Documents", [])

        if not isinstance(type_of_KYC, list) or not isinstance(types_of_Documents, list):
            return Response({"error": "'type_of_KYC' and 'types_of_Documents' must be lists"}, status=status.HTTP_400_BAD_REQUEST)

        # Assign license
        assigned_at = datetime.utcnow()
        license_assignments_collection.insert_one({
            "license_id": data["license_id"],
            "recipient_email": data["recipient_email"],
            "assigned_at": assigned_at,
            "type_of_KYC": type_of_KYC,
            "types_of_Documents": types_of_Documents,
            "status": "pending"
        })

        # Update used slots
        updated_slots = license_entry["used_slots"] + 1
        update_data = {"used_slots": updated_slots}

        # If all slots are used, mark as expired
        if updated_slots >= license_entry["total_slots"]:
            update_data["status"] = "expired"

        licenses_collection.update_one({"_id": data["license_id"]}, {"$set": update_data})

         # Send email notification
        send_license_assignment_email(
            recipient_email=data["recipient_email"],
            license_type=license_entry["license_type"],
            assigned_at=assigned_at,
            initiator_email=license_entry["initiator_email"]
        )

        return Response({"message": "License assigned successfully!"}, status=status.HTTP_201_CREATED)


# Check License Status
class LicenseStatusView(APIView):
    def get(self, request, license_id):
        license_entry = licenses_collection.find_one({"_id": license_id})
        if not license_entry:
            return Response({"error": "License not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"license_status": license_entry["status"]}, status=status.HTTP_200_OK)