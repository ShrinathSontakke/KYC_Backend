# from django.test import TestCase
# from .db_mongo import licenses_collection

# class LicenseAPITestCase(TestCase):
#     def test_license_creation(self):
#         license_data = {
#             "initiator_id": "user123",
#             "license_type": "Basic",
#             "total_slots": 5,
#             "valid_until": "2025-12-31",
#             "purchase_date": "2024-01-30",
#             "status": "active",
#             "used_slots": 0
#         }
#         licenses_collection.insert_one(license_data)
#         self.assertIsNotNone(licenses_collection.find_one({"initiator_id": "user123"}))
