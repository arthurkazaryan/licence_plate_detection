from django.contrib import admin
from text_comparison.models import UserComparisons


@admin.register(UserComparisons)
class UserComparisonsAdmin(admin.ModelAdmin):
    list_display = ('user', 'comparison_uuid', 'text', 'nearest_text', 'similarity', 'date')
    # readonly_fields = ('user', 'comparison_uuid', 'text', 'nearest_text', 'similarity', 'date')
    search_fields = ('user__username',)
