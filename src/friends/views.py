from django.shortcuts import redirect, render
from django.http import HttpResponse
import json
from users.models import User
from friends.models import FriendRequest

def friend_request_view(request, *args, **kwargs):
    context = {}
    curr_user = request.user
    if curr_user.is_authenticated:
        user_id = kwargs.get("user_id")
        user = User.objects.get(pk=user_id)
        if user == curr_user:
            friend_requests = FriendRequest.objects.filter(receiver=user, pending=True)
            context['friend_requests'] = friend_requests
        else:
            return HttpResponse("You may only view your friend requests")
    else:
        redirect("login")
    return render(request, "friends/friend_requests.html", context)

def send_friend_request(request, *args, **kwargs):
    user = request.user
    ajax_content = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = User.objects.get(pk=user_id)
            try:
                friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
                try:
                    for f_request in friend_requests:
                        if f_request.pending:
                            raise Exception("Friend request already sent.")
                    friend_request = FriendRequest(sender=user, receiver=receiver)
                    friend_request.save()
                    ajax_content['result'] = "success"
                    ajax_content['response'] = "Friend request sent"
                except Exception as e:
                    ajax_content['result'] = "error"
                    ajax_content['response'] = str(e)
            except FriendRequest.DoesNotExist:
                friend_request = FriendRequest(sender=user, receiver=receiver)
                friend_request.save()
                ajax_content['result'] = "success"
                ajax_content['response'] = "Friend request sent"
            if ajax_content["response"] == None:
                ajax_content['result'] = "error"
                ajax_content['response'] = "Something went wrong"
        else:
            ajax_content['result'] = "error"
            ajax_content['response'] = "Unable to send friend request"
    else:
        ajax_content['result'] = "error"
        ajax_content['response'] = "You must be logged in to send a friend request"
    return HttpResponse(json.dumps(ajax_content), content_type="application/json")