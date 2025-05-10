from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from allauth.account.forms import SignupForm
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def custom_login_view(request):
    if request.user.is_authenticated:
        return redirect('/')  # Already logged in, redirect to homepage

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())  # Log the user in
            return redirect('/')  # Redirect to the homepage
    else:
        form = AuthenticationForm()  # Create an empty form on GET request

    return render(request, 'users/custom_login.html', {'form': form})


@csrf_protect
def custom_signup_view(request):
    if request.user.is_authenticated:
        return redirect('/')  # Redirect to homepage if already logged in

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user without the request context (it will handle the email)
            login(request, user)  # Automatically log the user in after successful signup
            return redirect('/')  # Redirect to homepage after successful signup
    else:
        form = SignupForm()  # Create an empty form on GET request

    return render(request, 'users/custom_signup.html', {'form': form})


@csrf_protect
def custom_logout_view(request):
    if request.method == 'POST':
        logout(request)  # Logout the user
        return redirect('/')  # Redirect to homepage after logout
    return render(request, 'users/logout_confirm.html')  # Optional confirmation page
