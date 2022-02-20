from django.shortcuts import redirect, render
from django.http import HttpResponse
import json
from userposts.models import UserPost
from users.models import User
from friends.models import FriendList

def home_page(request, *args, **kwargs):
    context = {}
    curr_user = request.user
    if request.method == "POST" and curr_user.is_authenticated:
        pass

    # request.method GET
    friend_list = []
    try:
        curr_user_friend_list = FriendList.objects.get(user=curr_user)
        for friend in curr_user_friend_list.friends.all():
            friend_list.append(friend)
    except FriendList.DoesNotExist:
        pass

    if friend_list != []:
        # include curr user to list before filtering
        friend_list.append(curr_user)
        # display own post + friends' posts
        # filter UserPost based on poster = current user
        posts = UserPost.objects.filter(poster__in=friend_list)
        context['posts'] = posts
        
        # Group.objects.filter(player__name__in=['Player1','Player2'])
        # UserPost.objects.filter(poster__in=[])
    else:
        # display own posts only
        posts = UserPost.objects.filter(poster=curr_user)
        context['posts'] = posts
    return render(request, "userposts/homepage.html", context)
    # filter 


    # form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
    #     image_updated = False
    #     # retrieve file if it exissts
    #     if 'profile_image_file_selector' in request.FILES:

    #         request_file = request.FILES['profile_image_file_selector'] 
    #         # default path of settings.MEDIA_ROOT
    #         url = os.path.join(settings.MEDIA_ROOT + "/", str(user.pk))
    #         fss = FileSystemStorage(location=url)
    #         user.profile_img.delete()
    #         file = fss.save("profile_image.png", request_file)
    #         user.profile_img = f"{str(user.pk)}/profile_image.png"
    #         user.save()
    #         image_updated = True
    #     if form.is_valid():
    #         form.save()
    #         return redirect("users:user_profile", user_id=user.pk)
    #     elif image_updated:
    #         print("image updated")
    #         return redirect("users:user_profile", user_id=user.pk)
    #     else:
    #         form = UserUpdateForm(request.POST, instance=request.user,
    #             initial = {
    #                 "id": user.pk,
    #                 "email": user.email,
    #                 "username": user.username,
    #                 "profile_img": user.profile_img,
    #             }
    #         )
    #         context['form'] = form
    # else:
    #     form = UserUpdateForm(
    #         initial = {
    #             "id": user.pk,
    #             "email": user.email,
    #             "username": user.username,
    #             "profile_img": user.profile_img,
    #         }
    #     )
    #     context['form'] = form


    # try:
    #     viewed_user = User.objects.get(pk=userid_search)
    # except User.DoesNotExist:
    #     return HttpResponse("No user of this id found.")
    # if User:
    #     context['id'] = viewed_user.id
    #     context['email'] = viewed_user.email
    #     context['username'] = viewed_user.username
    #     context['profile_img'] = viewed_user.profile_img.url
        
    #     try:
    #         friend_list = FriendList.objects.get(user=viewed_user)
    #     except FriendList.DoesNotExist:
    #         friend_list = FriendList(user=viewed_user)
    #         friend_list.save()
    #     friends = friend_list.friends.all()
    #     context['friends'] = friends

    #     is_self = True
    #     is_friend = False
    #     curr_user = request.user
    #     friend_requests = None
    #     request_sent = FriendRequestStatus.NO_FRIEND_REQUEST.value
    #     # NO_FRIEND_REQUEST = 0
    #     # FRIEND_REQUEST_TO_USER = 1
    #     # FRIEND_REQUEST_FROM_USER = 2
    #     if (curr_user.is_authenticated and curr_user != viewed_user):
    #         is_self = False
    #         if friends.filter(pk=curr_user.id):
    #             is_friend = True
    #         else:
    #             is_friend = False
    #             if friend_request_exists(sender=viewed_user, receiver=curr_user) != False:
    #                 request_sent = FriendRequestStatus.FRIEND_REQUEST_TO_USER.value
    #                 context['pending_friend_request_id'] = friend_request_exists(sender=viewed_user, receiver=curr_user).id
    #             elif friend_request_exists(sender=curr_user, receiver=viewed_user) != False:
    #                 request_sent = FriendRequestStatus.FRIEND_REQUEST_FROM_USER.value
    #             else:
    #                 request_sent = FriendRequestStatus.NO_FRIEND_REQUEST.value
    #     elif not curr_user.is_authenticated:
    #         is_self = False
    #     else:
    #         try:
    #             friend_requests = FriendRequest.objects.filter(receiver=curr_user, pending=True)
    #         except:
    #             pass

    #     context['is_self'] = is_self
    #     context['is_friend'] = is_friend
    #     context['BASE_URL'] = settings.BASE_URL
    #     context['request_sent'] = request_sent
    #     context['friend_requests'] = friend_requests
