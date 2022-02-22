# from django.db import models
# from django.conf import settings

# class ChatList(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
#     chatrooms = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="chatrooms")

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

# class ChatRoom(models.Model):
#     host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     guest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
