from django.urls import path
from accounts.views import RegisterUser, LoginUser, logout_user, ProfilePage


urlpatterns = [
    path('home/', ProfilePage.as_view(), name='accounts-home'),
    path('register/', RegisterUser.as_view(), name='accounts-register'),
    path('login/', LoginUser.as_view(), name='accounts-login'),
    path('logout/', logout_user, name='accounts-logout')
]
