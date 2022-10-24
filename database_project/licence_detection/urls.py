from django.urls import path
from licence_detection.views import LicenceDetectionPage, LicenceDetectionView


urlpatterns = [
    path('home/', LicenceDetectionPage.as_view(), name='licence_detection-home'),
    path('view/<str:uuid>', LicenceDetectionView.as_view(), name='licence_detection-view')
]
