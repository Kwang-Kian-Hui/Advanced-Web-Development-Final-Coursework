from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from friendchat.models import Channel, Message
from users.models import User

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
    context['curr_user'] = curr_user
    context['channel'] = channel
    context['friend'] = friend
    context['message'] = channel.message_set.all()
    if request.method == "POST":
        content = request.POST.get("message")
        Message.objects.create(sender=curr_user, channel=channel, content=content)
        channel = Channel.objects.get_or_create_personal_channel(curr_user, friend)
        context['channel'] = channel
        context['message'] = channel.message_set.all()
        return render(request, "friendchat/chat.html", context=context)
    return render(request, "friendchat/chat.html", context=context)

# class ChatView(View):

#     def get_queryset(self):
#         return Channel.objects.by_user(self.request.user)

#     def get_object(self):
#         friend_username  = self.kwargs.get("username")
#         self.friend = User.objects.get(username=friend_username)
#         obj = Channel.objects.get_or_create_personal_channel(self.request.user, self.other_user)
#         if obj == None:
#             raise Http404
#         return obj

#     def get_context_data(self, **kwargs):
#         context = {}
        
#         return context

#     def get(self, request, **kwargs):
#         context = self.get_context_data(**kwargs)
#         return render(request, "friendchat/chat.html", context=context)

#     def post(self, request, **kwargs):
#         self.object = self.get_object()
#         channel = self.get_object()
#         curr_user = request.user
#         content = request.POST.get("message")
#         Message.objects.create(sender=curr_user, channel=channel, content=content)
#         context = self.get_context_data(**kwargs)
#         return render(request, "friendchat/chat.html", context=context)