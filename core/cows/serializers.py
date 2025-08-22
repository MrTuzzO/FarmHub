from rest_framework import serializers
from .models import Cow
from accounts.models import User


class CowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cow
        fields = ['id', 'tag', 'breed', 'farm', 'owner', 'dob', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # only users with role 'farmer' in owner field
        self.fields['owner'].queryset = User.objects.filter(role=User.FARMER)