from django.urls import path
from .views import custom_login_view, custom_signup_view, custom_logout_view

urlpatterns = [
    path('login/', custom_login_view, name='custom_login'),
    path('signup/', custom_signup_view, name='custom_signup'),
    path('logout/', custom_logout_view, name='custom_logout'),
]
