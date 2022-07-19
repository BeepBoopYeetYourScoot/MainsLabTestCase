from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Bill


class BillSerializer(serializers.ModelSerializer):
    """
    Serializer for the Bills
    """
    class Meta:
        model = Bill
        fields = '__all__'

    def validate_service(self, value):
        """
        Additional validation for the 'service' field
        """
        if value == '-':
            raise ValidationError('Service cannot be empty')
        return value
