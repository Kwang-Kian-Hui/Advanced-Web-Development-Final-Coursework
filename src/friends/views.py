from django.shortcuts import redirect, render
from django.http import HttpResponse
import json
from users.models import User
from friends.models import FriendList, FriendRequest

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
    curr_user = request.user
    ajax_content = {}
    if request.method == "POST" and curr_user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = User.objects.get(pk=user_id)
            try:
                friend_requests = FriendRequest.objects.filter(sender=curr_user, receiver=receiver)
                try:
                    for f_request in friend_requests:
                        if f_request.pending:
                            raise Exception("Friend request already sent.")
                    friend_request = FriendRequest(sender=curr_user, receiver=receiver)
                    friend_request.save()
                    ajax_content['result'] = "success"
                    ajax_content['response'] = "Friend request sent"
                except Exception as e:
                    ajax_content['result'] = "error"
                    ajax_content['response'] = "An error occured. Failed to send request"
            except FriendRequest.DoesNotExist:
                friend_request = FriendRequest(sender=curr_user, receiver=receiver)
                friend_request.save()
                ajax_content['result'] = "success"
                ajax_content['response'] = "Friend request sent"
            if ajax_content["response"] == None:
                ajax_content['result'] = "error"
                ajax_content['response'] = "An error occured. Failed to send request"
        else:
            ajax_content['result'] = "error"
            ajax_content['response'] = "Something went wrong"
    else:
        ajax_content['result'] = "error"
        ajax_content['response'] = "You must be logged in to send a friend request"
    return HttpResponse(json.dumps(ajax_content), content_type="application/json")

def accept_friend_request(request, *args, **kwargs):
    curr_user = request.user
    ajax_content = {}
    if request.method == "GET" and curr_user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id != None:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            if friend_request.receiver == curr_user:
                if friend_request:
                    friend_request.accept()
                    ajax_content['result'] = "success"
                    ajax_content['response'] = "Friend request accepted"
                else:
                    ajax_content['result'] = "error"
                    ajax_content['response'] = "An error occurred. Failed to decline request"
            else:
                ajax_content['result'] = "error"
                ajax_content["response"] = "You may only accept your own friend requests"
        else:
            ajax_content['result'] = "error"
            ajax_content["response"] = "No friend request of such id found"
    else:
        ajax_content['result'] = "error"
        ajax_content["response"] = "You must be logged in to accept a friend request"
    return HttpResponse(json.dumps(ajax_content), content_type="application/json")

def decline_friend_request(request, *args, **kwargs):
    curr_user = request.user
    ajax_content = {}
    if request.method == "GET" and curr_user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            if friend_request.receiver == curr_user:
                if friend_request:
                    friend_request.decline()
                    ajax_content['result'] = "success"
                    ajax_content['response'] = "Friend request declined"
                else:
                    ajax_content['result'] = "error"
                    ajax_content['response'] = "An error occurred. Please try again later"
            else:
                ajax_content['result'] = "error"
                ajax_content['response'] = "You may only decline requests that you received"
        else:
            ajax_content['result'] = "error"
            ajax_content['response'] = "No friend request of such id found"
    else:
        ajax_content['result'] = "error"
        ajax_content['response'] = "You must be logged in to decline a friend request"
    return HttpResponse(json.dumps(ajax_content), content_type="application/json")

def cancel_friend_request(request, *args, **kwargs):
    curr_user = request.user
    ajax_content = {}
    if request.method == "POST" and curr_user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = User.objects.get(pk=user_id)
            try:
                friend_requests_by_curr_user = FriendRequest.objects.filter(sender=curr_user, receiver=receiver, pending=True)
            except Exception as e:
                ajax_content['result'] = "error"
                ajax_content['response'] = "An error occurred. No friend requests to cancel"
            # should only have 1 such request as each user can only send 1 request to another specific user
            # however we should still check to ensure that all requests to that specific user is cancelled
            if len(friend_requests_by_curr_user) > 1:
                for request in friend_requests_by_curr_user:
                    request.cancel()
                ajax_content['result'] = "success"
                ajax_content['response'] = "Friend request cancelled"
            else:
                friend_requests_by_curr_user.first().cancel()
                ajax_content['result'] = "success"
                ajax_content['response'] = "Friend request cancelled"
        else:
            ajax_content['result'] = "error"
            ajax_content['response'] = "An error occurred. No user of such id found"
    else:
        ajax_content['result'] = "error"
        ajax_content['response'] = "You must be logged in to cancel a friend request"
    return HttpResponse(json.dumps(ajax_content), content_type="application/json")


def remove_friend(request, *args, **kwargs):
    user = request.user
    ajax_content = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            try:
                user_to_remove = User.objects.get(pk=user_id)
                self_friend_list = FriendList.objects.get(user=user)
                self_friend_list.unfriend(user_to_remove)
                ajax_content['result'] = "success"
                ajax_content['response'] = "Friend removed successfully"
            except Exception as e:
                ajax_content['result'] = "error"
                ajax_content['response'] = "An error occurred. Failed to remove friend"
        else:
            ajax_content['result'] = "error"
            ajax_content['response'] = "Something went wrong. Unable to remove friend"
    else:
        ajax_content['result'] = "error"
        ajax_content['response'] = "You must be logged in to remove a friend"
    return HttpResponse(json.dumps(ajax_content), content_type="application/json")
