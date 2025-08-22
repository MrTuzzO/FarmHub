from rest_framework import viewsets, permissions
from .models import Activity
from .serializers import ActivitySerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all().order_by('-date')
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superadmin():
            return Activity.objects.all()
        if user.is_agent():
            return Activity.objects.filter(cow__farm__agent=user)
        if user.is_farmer():
            return Activity.objects.filter(performed_by=user)
        return Activity.objects.none()

    def perform_create(self, serializer):
        """Auto-set performed_by to current farmer"""
        user = self.request.user
        if user.is_farmer():
            serializer.save(performed_by=user)
        else:
            serializer.save()
