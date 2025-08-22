from django.contrib import admin
from .models import Farm
from cows.models import Cow
from milk.models import MilkRecord
from activities.models import Activity


class CowInline(admin.TabularInline):
    model = Cow
    extra = 0
    fields = ('tag', 'breed', 'owner', 'dob')
    readonly_fields = ()


class MilkRecordInline(admin.TabularInline):
    model = MilkRecord
    extra = 0
    fields = ('cow', 'date', 'quantity_liters', 'recorded_by')
    readonly_fields = ('recorded_by',)


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'agent', 'cow_count', 'created_at')
    list_filter = ('agent', 'created_at')
    search_fields = ('name', 'location', 'agent__username', 'agent__first_name', 'agent__last_name')
    inlines = [CowInline]
    
    def cow_count(self, obj):
        return obj.cows.count()
    cow_count.short_description = 'Number of Cows'
