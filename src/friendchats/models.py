from django.db import models
from django.conf import settings

class ChatRoom(models.Model):
    chatroom_name = models.CharField(max_length=255, unique=True, blank=True)
    participant1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    participant2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class ChatLog(models.Model):
    chatlog = models.TextField(unique=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.chatroom_name
    
#     def connect_user(self, users_to_add):
#         # users_to_add includes request user and user's friend
#         user_added = False
#         if not user_to_add in self.participants.all():
#             self.participants.add(user_to_add)
#             self.save()
#             user_added = True
#         elif user_to_add in self.participants.all():
#             user_added = True
#         return user_added

# class ChatList(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
#     chatrooms = models.ManyToManyField(ChatRoom, blank=True, related_name="chatrooms")

#     def __str__(self):
#         return self.user.username

#     def create_chat(self, user_to_add):
#         chat_room_id = f"{str(int(self.user.id) * 4 - 4)}{str(int(user_to_add.id) * 3 - 5)}chatroom{self.user.username}"
#         if not chat_room_id in self.chatrooms.all():
#             self.chatrooms.add(chat_room_id)
#         pass
        
#         # if not user_to_add in self.friends.all():
#         #     self.friends.add(user_to_add)
    
#     def delete_chat(self, user_to_remove):
#         pass
#         # if user_to_remove in self.friends.all():
#         #     self.friends.remove(user_to_remove)

#     # def unfriend(self, user_to_remove):
#     #     self.remove_friend(user_to_remove)

#     #     removed_user = FriendList.objects.get(user=user_to_remove)
#     #     # removed_user.remove_user(self.user)
#     #     removed_user.remove_friend(self.user)
