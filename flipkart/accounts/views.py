from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import update_session_auth_hash


def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect('register')

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                'Username already exists.'
            )

            return redirect('register')

        if User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                'Email already registered.'
            )

            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        Profile.objects.create(
            user=user
        ) 

        user.save()

        messages.success(
            request,
            'Registration successful. Please login.'
        )

        return redirect('login')

    return render(
        request,
        'accounts/register.html'
    )

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        messages.error(
            request,
            'Invalid username or password.'
        )

        return redirect('login')

    return render(
        request,
        'accounts/login.html'
    )


def user_logout(request):

    logout(request)

    return redirect('home')

@login_required(login_url='login')
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        'accounts/profile.html',
        {
            'profile': profile,
        }
    )

@login_required(login_url='login')
def profile_edit(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        profile.full_name = request.POST.get('full_name')
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.city = request.POST.get('city')
        profile.state = request.POST.get('state')
        profile.pincode = request.POST.get('pincode')

        if request.FILES.get('profile_image'):
            profile.profile_image = request.FILES.get('profile_image')

        profile.save()

        messages.success(
            request,
            'Profile updated successfully.'
        )

        return redirect('profile')

    return render(
        request,
        'accounts/profile_edit.html',
        {
            'profile': profile,
        }
    )

@login_required(login_url='login')
def change_password(request):

    if request.method == 'POST':

        current_password = request.POST.get(
            'current_password'
        )

        new_password = request.POST.get(
            'new_password'
        )

        confirm_password = request.POST.get(
            'confirm_password'
        )

        # Current password check

        if not request.user.check_password(
            current_password
        ):

            messages.error(
                request,
                'Current password is incorrect.'
            )

            return redirect('change_password')


        # New password match

        if new_password != confirm_password:

            messages.error(
                request,
                'New passwords do not match.'
            )

            return redirect('change_password')


        # Password length

        if len(new_password) < 8:

            messages.error(
                request,
                'Password must be at least 8 characters.'
            )

            return redirect('change_password')


        # Change password

        request.user.set_password(
            new_password
        )

        request.user.save()


        # Keep user logged in

        update_session_auth_hash(
            request,
            request.user
        )


        messages.success(
            request,
            'Password changed successfully.'
        )

        return redirect('profile')


    return render(
        request,
        'accounts/change_password.html'
    )




