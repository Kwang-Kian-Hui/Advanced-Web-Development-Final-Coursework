from django.shortcuts import render

def chatroom_list_view(request, *args, **kwargs):
    context = {}
    curr_user = request.user
    return render(request, 'friendchats/friend_chat_list.html', context)