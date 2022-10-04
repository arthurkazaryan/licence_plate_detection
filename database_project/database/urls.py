from django.urls import path
from database.views import index


urlpatterns = [
    path('', index, name='database-home'),
]
