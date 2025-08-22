from django.contrib import admin
from .models import MilkRecord


@admin.register(MilkRecord)
class MilkRecordAdmin(admin.ModelAdmin):
    list_display = ('cow', 'date', 'quantity_liters', 'recorded_by', 'farm_name')
    list_filter = ('date', 'cow__farm', 'recorded_by', 'cow__breed')
    search_fields = ('cow__tag', 'recorded_by__username', 'cow__farm__name')
    list_select_related = ('cow', 'recorded_by', 'cow__farm')
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Milk Record', {
            'fields': ('cow', 'date', 'quantity_liters', 'recorded_by')
        }),
    )
    
    def farm_name(self, obj):
        return obj.cow.farm.name if obj.cow and obj.cow.farm else "Unknown"
    farm_name.short_description = 'Farm'
