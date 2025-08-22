from django.db import models
from django.conf import settings
from cows.models import Cow


class Activity(models.Model):
    VACCINATION = 'vaccination'
    BIRTH = 'birth'
    HEALTH_CHECK = 'health_check'
    OTHER = 'other'

    ACTIVITY_TYPES = [
        (VACCINATION, 'Vaccination'),
        (BIRTH, 'Birth'),
        (HEALTH_CHECK, 'Health Check'),
        (OTHER, 'Other'),
    ]

    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='activities')
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    activity_type = models.CharField(max_length=64, choices=ACTIVITY_TYPES)
    notes = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_activity_type_display()} for {self.cow} on {self.date}"
