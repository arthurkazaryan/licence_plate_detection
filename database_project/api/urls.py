from django.urls import path
from api import views

urlpatterns = [
    path('v1/post/licence_plate', views.post_licence_plate),
]
