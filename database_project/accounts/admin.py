from django.contrib import admin
from django.contrib.admin import display
from accounts.models import UserCamera, UserSnapshotProject, UserSnapshotItem


@admin.register(UserCamera)
class UserCameraAdmin(admin.ModelAdmin):
    list_display = ('user', 'camera_uuid', 'rtsp_address', 'date')
    # readonly_fields = ('user', 'camera_uuid', 'rtsp_address', 'date')
    search_fields = ('user__username',)


@admin.register(UserSnapshotProject)
class UserSnapshotProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'camera', 'project_uuid', 'image', 'date')
    # readonly_fields = ('user', 'project_uuid', 'image', 'date')
    search_fields = ('user__username',)


@admin.register(UserSnapshotItem)
class UserSnapshotItemAdmin(admin.ModelAdmin):
    list_display = ('project', 'shapshot_uuid', 'color', 'plate_number', 'date')
    # readonly_fields = ('project', 'shapshot_uuid', 'color', 'plate_number', 'date')
