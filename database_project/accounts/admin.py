from django.contrib import admin
from django.contrib.admin import display
from accounts.models import UserCamera, UserSnapshot


@admin.register(UserCamera)
class UserCameraAdmin(admin.ModelAdmin):
    list_display = ('user', 'camera_uuid', 'rtsp_address', 'date')
    # readonly_fields = ('user', 'camera_uuid', 'rtsp_address', 'date')
    search_fields = ('user__username',)


@admin.register(UserSnapshot)
class UserSnapshotAdmin(admin.ModelAdmin):
    list_display = ('user', 'camera', 'image_uuid', 'image', 'date')
    # readonly_fields = ('user', 'camera', 'image_uuid', 'image', 'date')
    search_fields = ('user__username',)
