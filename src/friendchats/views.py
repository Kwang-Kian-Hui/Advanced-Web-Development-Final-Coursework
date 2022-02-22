from django.shortcuts import render
from django.db.models import Q
from friendchats.models import ChatRoom

def chatroom_list_view(request, *args, **kwargs):
    context = {}
    curr_user = request.user
    curr_user_chatrooms = ChatRoom.objects.filter(Q(participant1=curr_user) | Q(participant2=curr_user))
    context['chatrooms'] = curr_user_chatrooms
    return render(request, 'friendchats/friend_chat_list.html', context)

def chatroom_view(request, *args, **kwargs):
    context = {}
    curr_user = request.user
    # context['room_name'] = kwargs.get("room_name")

    return render(request, 'friendchats/friend_chat.html', context)