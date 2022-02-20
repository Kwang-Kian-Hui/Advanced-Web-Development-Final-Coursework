from django.shortcuts import redirect, render
from django.http import HttpResponse
import json
from userposts.models import UserPost
from users.models import User
from friends.models import FriendList

def home_page(request, *args, **kwargs):
    context = {}
    curr_user = request.user
    friend_list = []
    try:
        curr_user_friend_list = FriendList.objects.get(user=curr_user)
        for friend in curr_user_friend_list.friends.all():
            friend_list.append(friend)
    except FriendList.DoesNotExist:
        pass

    if friend_list != []:
        # display own post + friends'
        pass
    else:
        # display own posts only
        # UserPost.objects.get()
        pass
    # filter 

    # filter UserPost based on poster = current user
    # Group.objects.filter(player__name__in=['Player1','Player2'])
    # UserPost.objects.filter(poster__in=[])


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

        
    return render(request, "userposts/homepage.html", context)