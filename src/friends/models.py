from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.utils import timezone

class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends")

    def __str__(self):
        return self.user.username

    def add_friend(self, user_to_add):
        if not user_to_add in self.friends.all():
            self.friends.add(user_to_add)
    
    def remove_friend(self, user_to_remove):
        if user_to_remove in self.friends.all():
            self.friends.remove(user_to_remove)

    def unfriend(self, user_to_remove):
        # self_user = self
        # self_user.remove_friend(user_to_remove)
        self.remove_friend(user_to_remove)

        removed_user = FriendList.objects.get(user=user_to_remove)
        removed_user.remove_user(self.user)

    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False

class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
    pending = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username
    
    def accept(self):
        receiver_friends = FriendList.objects.get(user=self.receiver)
        if receiver_friends:
            receiver_friends.add_friend(self.sender)
            sender_friends = FriendList.objects.get(user=self.sender)
            sender_friends.add_friend(self.receiver)
            self.pending = False
            self.save()
    
    def decline(self):
        self.pending = False
        self.save()

    def cancel(self):
        self.pending = False
        self.save()