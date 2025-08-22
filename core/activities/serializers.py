from rest_framework import serializers
from .models import Activity
from accounts.models import User

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'cow', 'performed_by', 'activity_type', 'notes', 'date', 'created_at']
        read_only_fields = ['created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # only users with role 'farmer' in performed_by field
        self.fields['performed_by'].queryset = User.objects.filter(role=User.FARMER)
