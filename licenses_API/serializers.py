from rest_framework import serializers

class LicenseSerializer(serializers.Serializer):
    initiator_id = serializers.CharField(required=True)
    license_type = serializers.ChoiceField(choices=["Basic", "Premium", "Enterprise"])
    total_slots = serializers.IntegerField(min_value=1)
    validity_period = serializers.CharField(required=False)
    status = serializers.ChoiceField(choices=["active", "expired"])
    used_slots = serializers.IntegerField(default=0)

class LicenseAssignmentSerializer(serializers.Serializer):
    license_id = serializers.CharField(required=True)
    recipient_email = serializers.EmailField(required=True)
    