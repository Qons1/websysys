from django.contrib import admin
from .models import Badge, UserBadge, UserProfile

admin.site.register(Badge)
admin.site.register(UserBadge)
admin.site.register(UserProfile)
