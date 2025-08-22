from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Farm
from .serializers import FarmSerializer


class IsAgentOrSuper(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_superadmin() or request.user.is_agent())

    def has_object_permission(self, request, view, obj):
        # agents can only manage their assigned farms
        if request.user.is_superadmin():
            return True
        if request.user.is_agent():
            return obj.agent_id == request.user.id
        return False


class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all().order_by('id')
    serializer_class = FarmSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAgentOrSuper(),]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.is_superadmin():
            return Farm.objects.all()
        if user.is_agent():
            return Farm.objects.filter(agent=user)
        return Farm.objects.none()

    def perform_create(self, serializer):
        """Auto-assign farm to the agent who creates it"""
        user = self.request.user
        if user.is_agent():
            serializer.save(agent=user)
        else:
            serializer.save()
