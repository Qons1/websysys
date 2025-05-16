"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Homepage (base page)
    path('', TemplateView.as_view(template_name='base.html'), name='home'),

    # Allauth URLs for authentication
    path('accounts/', include('allauth.urls')),\
    
    path('users/', include('users.urls')),

    # Items URLs
    path('items/', include('items.urls')),

    # Optional: add custom user profile or dashboard
    # path('profile/', include('users.urls')),  # Uncomment if you have a profile page
]

