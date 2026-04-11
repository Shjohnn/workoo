import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _

from .forms import RegisterForm, ProfileEditForm
from .models import UserProfile
from ratings.models import Rating


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            role = request.POST.get('role', 'worker')
            if role not in ('worker', 'employer'):
                role = 'worker'
            user = form.save(role=role)
            login(request, user)
            messages.success(
                request,
                _('Welcome, %(name)s! Your account was created successfully.') % {
                    'name': user.first_name or user.username,
                },
            )
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            error = _('Incorrect username or password.')
    return render(request, 'accounts/login.html', {'error': error})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def profile_view(request, pk=None):
    if pk:
        profile_user = get_object_or_404(User, pk=pk)
    else:
        if not request.user.is_authenticated:
            return redirect('login')
        profile_user = request.user

    profile = get_object_or_404(UserProfile, user=profile_user)
    ratings = Rating.objects.filter(worker=profile_user).select_related('employer', 'job')
    avg = profile.average_rating()
    posted_jobs = profile_user.posted_jobs.all()[:5] if profile.role == 'employer' else None
    applied_jobs = profile_user.applications.select_related('job').all()[:5] if profile.role == 'worker' else None

    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'ratings': ratings,
        'avg': avg,
        'posted_jobs': posted_jobs,
        'applied_jobs': applied_jobs,
        'is_own': request.user == profile_user,
    })


@login_required
def profile_edit_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data.get('email', '')
            request.user.save()
            form.save()
            messages.success(request, _('Profile updated successfully!'))
            return redirect('profile_own')
    else:
        form = ProfileEditForm(instance=profile, user=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
@require_POST
def set_theme_view(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'ok': False, 'error': 'invalid_json'}, status=400)
    theme = data.get('theme')
    if theme not in ('light', 'dark'):
        return JsonResponse({'ok': False, 'error': 'invalid_theme'}, status=400)
    profile = request.user.profile
    profile.theme_preference = theme
    profile.save(update_fields=['theme_preference'])
    return JsonResponse({'ok': True})
