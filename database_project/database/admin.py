from django.contrib import admin
from database.models import CameraData


@admin.register(CameraData)
class CameraDataAdmin(admin.ModelAdmin):
    list_display = ('camera_id', 'direction', 'color', 'vehicle_type', 'number', 'date')
    # readonly_fields = ('camera_id',)
    # search_fields = ('',)
