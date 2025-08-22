from django.db import models
from django.conf import settings
from farms.models import Farm


class Cow(models.Model):
    tag = models.CharField(max_length=64)
    breed = models.CharField(max_length=128, blank=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='cows')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='cows')
    dob = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('farm', 'tag')

    def __str__(self):
        return f"{self.tag} ({self.breed})" if self.breed else self.tag
