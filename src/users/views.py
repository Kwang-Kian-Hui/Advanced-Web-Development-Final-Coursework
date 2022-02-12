from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from users.models import *
from users.forms import UserRegistrationForm, UserAuthenticationForm

def registration_view(request, *args, **kwargs):
    user = request.user

    if user.is_authenticated:
        return HttpResponse(f"You are already logged in as {user.email}.")
    context = {}

    if request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            # destination = kwargs.get("next")
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            # redirect(path_name) as defined in urls.py
            return redirect("home")
        else:
            context['registration_form'] = form
    return render(request, 'users/register.html', context)

def logout_view(request):
    logout(request)
    return redirect("home")

def login_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    if request.POST:
        form = UserAuthenticationForm(request.POST)
        
        if form.is_valid():
            form.save(request)
        #     email = form.cleaned_data.get('email').lower()
        #     password = form.cleaned_data.get('password')
        #     user = authenticate(email=email, password=password)
        #     if user:
        #         login(request, user)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect("home")
        else:
            context['login_form'] = form
    return render(request, "users/login.html", context)

def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect


def profile_view(request, *args, **kwargs):
    context = {}
    username_search = kwargs.get("username")
    try:
        user = User.objects.get(username=username_search)
    except User.DoesNotExist:
        return HttpResponse("No user of this username found.")
    if User:
        # context['id'] = user.id
        context['email'] = user.email
        context['username'] = user.username
        context['profile_img'] = user.profile_img.url
        
        is_self = True
        is_friend = False
        curr_user = request.user
        if (curr_user.is_authenticated and curr_user != user) or not curr_user.is_authenticated:
            is_self = False
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL

        return render(request, "users/profile.html", context)