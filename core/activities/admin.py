from django.contrib import admin
from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('cow', 'activity_type', 'date', 'performed_by', 'farm_name')
    list_filter = ('activity_type', 'date', 'cow__farm', 'performed_by')
    search_fields = ('cow__tag', 'notes', 'performed_by__username', 'cow__farm__name')
    list_select_related = ('cow', 'performed_by', 'cow__farm')
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Activity Details', {
            'fields': ('cow', 'activity_type', 'date', 'performed_by')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('wide',)
        }),
    )
    
    def farm_name(self, obj):
        return obj.cow.farm.name if obj.cow and obj.cow.farm else "Unknown"
    farm_name.short_description = 'Farm'
