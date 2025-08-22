from rest_framework import serializers
from .models import Farm
from accounts.models import User


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['id', 'name', 'location', 'agent', 'created_at']
        read_only_fields = ['created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        # only agent users in agent field and set read-only for agents
        self.fields['agent'].queryset = User.objects.filter(role=User.AGENT)
        if request and hasattr(request.user, 'is_agent') and request.user.is_agent():
            self.fields['agent'].read_only = True
