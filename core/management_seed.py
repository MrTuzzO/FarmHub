# Run it with: python manage.py shell < management_seed.py

from django.contrib.auth import get_user_model
from farms.models import Farm
from cows.models import Cow
from milk.models import MilkRecord
from activities.models import Activity
import datetime

User = get_user_model()

# create users
sa, _ = User.objects.get_or_create(username='superadmin', defaults={'email':'sa@example.com','role':User.SUPERADMIN})
sa.set_password('password')
sa.is_superuser = True
sa.is_staff = True
sa.save()

agent, _ = User.objects.get_or_create(username='agent1', defaults={'email':'agent1@example.com','role':User.AGENT})
agent.set_password('password')
agent.save()

farmer, _ = User.objects.get_or_create(username='farmer1', defaults={'email':'farmer1@example.com','role':User.FARMER})
farmer.set_password('password')
farmer.save()

farm, _ = Farm.objects.get_or_create(name='Green Farm', defaults={'location':'Riverside', 'agent': agent})

c1, _ = Cow.objects.get_or_create(tag='COW-001', farm=farm, defaults={'breed':'Local', 'owner':farmer})
c2, _ = Cow.objects.get_or_create(tag='COW-002', farm=farm, defaults={'breed':'Holstein', 'owner':farmer})

# milk records
MilkRecord.objects.get_or_create(cow=c1, date=datetime.date.today(), defaults={'recorded_by':farmer, 'quantity_liters':10})
MilkRecord.objects.get_or_create(cow=c2, date=datetime.date.today(), defaults={'recorded_by':farmer, 'quantity_liters':12.5})

# activities
Activity.objects.get_or_create(cow=c1, date=datetime.date.today(), defaults={'performed_by':farmer, 'activity_type':Activity.HEALTH_CHECK, 'notes':'Routine check'})
