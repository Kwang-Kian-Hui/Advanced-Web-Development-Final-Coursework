from re import I
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from friends.models import *
from friends.friend_request_status import *
from friends.utils import *
from users.models import *
from users.forms import UserRegistrationForm, UserAuthenticationForm, UserUpdateForm
import os

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
    userid_search = kwargs.get("user_id")
    try:
        viewed_user = User.objects.get(pk=userid_search)
    except User.DoesNotExist:
        return HttpResponse("No user of this id found.")
    if User:
        context['id'] = viewed_user.id
        context['email'] = viewed_user.email
        context['username'] = viewed_user.username
        context['profile_img'] = viewed_user.profile_img.url
        
        try:
            friend_list = FriendList.objects.get(user=viewed_user)
        except FriendList.DoesNotExist:
            friend_list = FriendList(user=viewed_user)
            friend_list.save()
        friends = friend_list.friends.all()
        context['friends'] = friends

        is_self = True
        is_friend = False
        curr_user = request.user
        # NO_FRIEND_REQUEST = 0
        # FRIEND_REQUEST_TO_USER = 1
        # FRIEND_REQUEST_FROM_USER = 2
        friend_requests = None
        request_sent = FriendRequestStatus.NO_FRIEND_REQUEST.value
        if (curr_user.is_authenticated and curr_user != viewed_user):
            is_self = False
            if friends.filter(pk=viewed_user.id):
                is_friend = True
            else:
                is_friend = False
                if friend_request_exists(sender=viewed_user, receiver=curr_user) != False:
                    request_sent = FriendRequestStatus.FRIEND_REQUEST_TO_USER.value
                    context['pending_friend_request_id'] = friend_request_exists(sender=viewed_user, receiver=curr_user).id
                
                elif friend_request_exists(sender=curr_user, receiver=viewed_user) != False:
                    request_sent = FriendRequestStatus.FRIEND_REQUEST_FROM_USER.value
                else:
                    request_sent = FriendRequestStatus.NO_FRIEND_REQUEST.value
        elif not curr_user.is_authenticated:
            is_self = False
        else:
            try:
                friend_requests = FriendRequest.objects.filter(receiver=curr_user, pending=True)
            except:
                pass

        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL
        context['request_sent'] = request_sent
        context['friend_requests'] = friend_requests

        return render(request, "users/profile.html", context)

def user_search_view(request, *args, **kwargs):
    context = {}
    if request.method == "GET":
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_results = User.objects.filter(username__icontains=search_query)
            profiles = []
            for result in search_results:
                profiles.append((result, False))
            context['profiles'] = profiles
    return render(request, "users/user_search.html", context)

def edit_user_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_userid = kwargs.get("user_id")
    try:
        user = User.objects.get(pk=user_userid)
    except User.DoesNotExist:
        return HttpResponse("An error occurred.")
    if user.pk != request.user.pk:
        return HttpResponse("Unable to edit another user's profile.")
    
    context = {}
    if request.POST:
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        image_updated = False
        # retrieve file if it exissts
        if 'profile_image_file_selector' in request.FILES:

            request_file = request.FILES['profile_image_file_selector'] 
            # default path of settings.MEDIA_ROOT
            url = os.path.join(settings.MEDIA_ROOT + "/", str(user.pk))
            fss = FileSystemStorage(location=url)
            user.profile_img.delete()
            file = fss.save("profile_image.png", request_file)
            user.profile_img = f"{str(user.pk)}/profile_image.png"
            user.save()
            image_updated = True
        if form.is_valid():
            form.save()
            return redirect("users:user_profile", user_id=user.pk)
        elif image_updated:
            print("image updated")
            return redirect("users:user_profile", user_id=user.pk)
        else:
            form = UserUpdateForm(request.POST, instance=request.user,
                initial = {
                    "id": user.pk,
                    "email": user.email,
                    "username": user.username,
                    "profile_img": user.profile_img,
                }
            )
            context['form'] = form
    else:
        form = UserUpdateForm(
            initial = {
                "id": user.pk,
                "email": user.email,
                "username": user.username,
                "profile_img": user.profile_img,
            }
        )
        context['form'] = form
    context['max_upload_memory_size'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    print("render edit user")
    return render(request, "users/edit_user.html", context)