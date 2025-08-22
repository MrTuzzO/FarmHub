from django.contrib import admin
from .models import Cow
from milk.models import MilkRecord
from activities.models import Activity


class MilkRecordInline(admin.TabularInline):
    model = MilkRecord
    extra = 0
    fields = ('date', 'quantity_liters', 'recorded_by')
    readonly_fields = ('recorded_by',)


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 0
    fields = ('activity_type', 'date', 'notes', 'performed_by')
    readonly_fields = ('performed_by',)


@admin.register(Cow)
class CowAdmin(admin.ModelAdmin):
    list_display = ('tag', 'breed', 'farm', 'owner', 'milk_records_count', 'latest_activity')
    list_filter = ('breed', 'farm', 'farm__agent', 'owner')
    search_fields = ('tag', 'breed', 'owner__username', 'farm__name')
    list_select_related = ('farm', 'owner')
    inlines = [MilkRecordInline, ActivityInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('tag', 'breed', 'farm', 'owner')
        }),
        ('Additional Details', {
            'fields': ('dob', 'notes'),
            'classes': ('collapse',)
        }),
    )
    
    def milk_records_count(self, obj):
        return obj.milk_records.count()
    milk_records_count.short_description = 'Milk Records'
    
    def latest_activity(self, obj):
        latest = obj.activities.first()
        return f"{latest.get_activity_type_display()} on {latest.date}" if latest else "None"
    latest_activity.short_description = 'Latest Activity'
