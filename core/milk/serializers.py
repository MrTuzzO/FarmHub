from rest_framework import serializers
from .models import MilkRecord


class MilkRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MilkRecord
        fields = ('id', 'cow', 'recorded_by', 'date', 'quantity_liters', 'created_at')
        read_only_fields = ('created_at', 'recorded_by')
