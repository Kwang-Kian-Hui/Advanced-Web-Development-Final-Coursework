from django.db import models
from django.db.models import Count
from django.conf import settings

class ChatManager(models.Manager):
    def get_or_create_personal_channel(self, user1, user2):
        channels = self.get_queryset()
        channels = channels.filter(users__in=[user1, user2]).distinct()
        channels = channels.annotate(u_count=Count('users')).filter(u_count=2)
        if channels.exists():
            return channels.first()
        else:
            
            channel_name = f"{user1.pk}{user1.email.split('@')[0]}{user2.pk}{user2.email.split('@')[0]}"
            channel = self.create(name=channel_name)
            channel.users.add(user1)
            channel.users.add(user2)
            return channel

    def by_user(self, user):
        return self.get_queryset().filter(users__in=[user])

class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Channel(TrackingModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    objects = ChatManager()

    def __str__(self) -> str:
        if self.users.count() == 2:
            return f'{self.users.first()} and {self.users.last()}'
        return f'{self.name}'

class Message(TrackingModel):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False)

    def __str__(self) -> str:
        return f'From <Channel - {self.channel}>'