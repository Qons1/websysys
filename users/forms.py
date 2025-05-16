from django import forms
from allauth.account.forms import SignupForm
from allauth.account.adapter import DefaultAccountAdapter

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Change placeholder for password2 field to remove redundant "(again)"
        self.fields['password2'].widget.attrs['placeholder'] = "Password"
        
class CustomAccountAdapter(DefaultAccountAdapter):
    """Custom account adapter to control badge assignment based on auth method"""
    def is_open_for_signup(self, request):
        # Allow signups
        return True
        
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        # Mark user as having a regular account (not verified with social auth)
        user.is_regular_account = True
        
        if commit:
            user.save()
        return user 