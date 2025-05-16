from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from users.models import UserProfile

class Command(BaseCommand):
    help = 'Set up user profiles and badge levels for all users'

    def handle(self, *args, **options):
        # Process all users
        users_count = 0
        google_users_count = 0
        
        for user in User.objects.all():
            profile, created = UserProfile.objects.get_or_create(user=user)
            
            # Check if Google user
            try:
                social_account = SocialAccount.objects.filter(user=user, provider='google').first()
                if social_account:
                    profile.is_google_user = True
                    if profile.badge_level < 1:
                        profile.badge_level = 1
                    profile.save()
                    google_users_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Set up Google profile for {user.username}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing {user.username}: {e}"))
                
            users_count += 1
        
        self.stdout.write(self.style.SUCCESS(f"Processed {users_count} users, found {google_users_count} Google users")) 