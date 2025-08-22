from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet
from farms.views import FarmViewSet
from cows.views import CowViewSet
from activities.views import ActivityViewSet
from milk.views import MilkViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'farms', FarmViewSet, basename='farm')
router.register(r'cows', CowViewSet, basename='cow')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'milk', MilkViewSet, basename='milk')

urlpatterns = router.urls
