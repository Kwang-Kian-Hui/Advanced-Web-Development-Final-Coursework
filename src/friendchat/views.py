from django.shortcuts import render
from django.http import HttpResponse
from friendchat.models import Channel, Message
from friends.models import FriendList
from users.models import User

def chat_list_view(request, *args, **kwargs):
    context = {}
    curr_user = request.user
    if not curr_user.is_authenticated:
        return HttpResponse("You must be logged in to chat with other users")

    friend_chat_list = []
    friends = FriendList.objects.get(user=curr_user)
    for friend in friends.friends.all():
        channel = Channel.objects.filter(users__in=[friend]).filter(users__in=[curr_user]).first()
        try:
            latest_message = Message.objects.filter(channel=channel).order_by('-pk').first().content
        except:
            latest_message = ''
        friend_chat_list.append([friend, latest_message])
    context['friend_chat_list'] = friend_chat_list
    return render(request, "friendchat/chatlist.html", context=context)

def chat_view(request, *args, **kwargs):
    context = {}
    curr_user = request.user
    if not curr_user.is_authenticated:
        return HttpResponse("You must be logged in to chat with other users")
    friend_id  = kwargs.get("friend_id")
    friend = User.objects.get(pk=friend_id)
    channel = Channel.objects.get_or_create_personal_channel(curr_user, friend)
    if channel == None:
        raise HttpResponse("An error occurred, could not send message")
    context['friend'] = friend
    context['room_name'] = channel.name
    context['channel'] = channel
    context['sender'] = curr_user.pk
    context['messages'] = Message.objects.filter(channel=channel)
    if request.method == "POST":
        content = request.POST.get("message")
        Message.objects.create(sender=curr_user, channel=channel, content=content)
        context['channel'] = channel
        context['messages'] = Message.objects.filter(channel=channel)
    return render(request, 'friendchat/chatroom.html', context)