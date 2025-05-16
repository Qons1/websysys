from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount

class Badge(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='badges/')

    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    badge_level = models.PositiveIntegerField(default=0)
    is_google_user = models.BooleanField(default=False)
    is_regular_account = models.BooleanField(default=False)
    post_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def calculate_badge_level(self):
        """Calculate badge level based on post count"""
        if self.is_regular_account and not self.is_google_user:
            self.badge_level = 0
            self.save()
            return 0
            
        self.badge_level = 1 + (self.post_count // 5)
        self.save()
        return self.badge_level

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create or update user profile when a user is created or saved"""
    # Get or create the profile
    profile, created_profile = UserProfile.objects.get_or_create(user=instance)
    
    # Check if user is a Google user (check every time, not just on creation)
    try:
        social_account = SocialAccount.objects.filter(user=instance, provider='google').first()
        if social_account:
            profile.is_google_user = True
            if profile.badge_level < 1:
                profile.badge_level = 1  # Start at level 1
            profile.save()
            print(f"Updated profile for Google user: {instance.username}")
        else:
            profile.is_regular_account = True
            profile.badge_level = 0
            profile.save()
    except Exception as e:
        print(f"Error checking for Google account: {e}")
