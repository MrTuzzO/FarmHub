from rest_framework import viewsets, permissions
from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MilkRecord
from .serializers import MilkRecordSerializer


class MilkViewSet(viewsets.ModelViewSet):
    queryset = MilkRecord.objects.all()
    serializer_class = MilkRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superadmin():
            return MilkRecord.objects.all()
        if user.is_agent():
            return MilkRecord.objects.filter(cow__farm__agent=user)
        if user.is_farmer():
            return MilkRecord.objects.filter(recorded_by=user)
        return MilkRecord.objects.none()

    def perform_create(self, serializer):
        """Auto-set recorded_by to current farmer"""
        user = self.request.user
        if user.is_farmer():
            serializer.save(recorded_by=user)
        else:
            serializer.save()

    @action(detail=False, methods=['get'])
    def aggregate(self, request):
        """Total milk within date range for current user's scope"""
        qs = self.get_queryset()
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        if start:
            qs = qs.filter(date__gte=start)
        if end:
            qs = qs.filter(date__lte=end)
        total = qs.aggregate(total_liters=Sum('quantity_liters'))
        return Response(total)

    @action(detail=False, methods=['get'])
    def by_farm(self, request):
        """Total milk production grouped by farm"""
        user = self.request.user
        if not (user.is_superadmin() or user.is_agent()):
            return Response({"detail": "Not permitted"}, status=403)
        
        qs = self.get_queryset()
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        if start:
            qs = qs.filter(date__gte=start)
        if end:
            qs = qs.filter(date__lte=end)
        
        from django.db.models import Sum
        farm_totals = qs.values('cow__farm__name', 'cow__farm__id').annotate(
            total_liters=Sum('quantity_liters')
        ).order_by('cow__farm__name')
        
        return Response(list(farm_totals))

    @action(detail=False, methods=['get'])
    def by_farmer(self, request):
        """Total milk production grouped by farmer"""
        user = self.request.user
        if not (user.is_superadmin() or user.is_agent()):
            return Response({"detail": "Not permitted"}, status=403)
        
        qs = self.get_queryset()
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        if start:
            qs = qs.filter(date__gte=start)
        if end:
            qs = qs.filter(date__lte=end)
        
        farmer_totals = qs.values('recorded_by__username', 'recorded_by__id').annotate(
            total_liters=Sum('quantity_liters')
        ).order_by('recorded_by__username')
        
        return Response(list(farmer_totals))
