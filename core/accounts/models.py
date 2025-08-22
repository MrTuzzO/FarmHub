from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    SUPERADMIN = 'superadmin'
    AGENT = 'agent'
    FARMER = 'farmer'

    ROLE_CHOICES = [
        (SUPERADMIN, 'SuperAdmin'),
        (AGENT, 'Agent'),
        (FARMER, 'Farmer'),
    ]


    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default=FARMER)

    def is_superadmin(self):
        return self.role == self.SUPERADMIN

    def is_agent(self):
        return self.role == self.AGENT

    def is_farmer(self):
        return self.role == self.FARMER
