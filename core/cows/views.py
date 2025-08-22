from rest_framework import viewsets, permissions
from .models import Cow
from .serializers import CowSerializer


class CowViewSet(viewsets.ModelViewSet):
    queryset = Cow.objects.all().order_by('id')
    serializer_class = CowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superadmin():
            return Cow.objects.all()
        if user.is_agent():
            # agents can see cows in their farms
            return Cow.objects.filter(farm__agent=user)
        if user.is_farmer():
            return Cow.objects.filter(owner=user)
        return Cow.objects.none()

    def perform_create(self, serializer):
        """Auto-set farmer as owner when they enroll their cows"""
        user = self.request.user
        if user.is_farmer():
            serializer.save(owner=user)
        else:
            serializer.save()
