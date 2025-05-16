from django.contrib.auth.models import User
from .models import UserProfile

def user_badges(request):
    """Add user badge information to all template contexts"""
    context = {}
    
    # Build a dictionary of user IDs to badge levels for all users
    user_badges = {}
    for profile in UserProfile.objects.filter(is_google_user=True):
        user_badges[profile.user_id] = profile.badge_level
    
    context['user_badges'] = user_badges
    return context 