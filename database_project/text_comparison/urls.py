from django.urls import path
from text_comparison.views import TextComparisonPage


urlpatterns = [
    path('home/', TextComparisonPage.as_view(), name='text_comparison-home'),
]
