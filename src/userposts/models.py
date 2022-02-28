import os
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.utils import timezone

def get_post_image_path(self):
    return os.path.join(settings.MEDIA_ROOT + "/", str(self.pk) + "/")

class UserPost(models.Model):
    content = models.TextField()
    img = models.ImageField(max_length=255, upload_to=get_post_image_path, null=True, blank=True)
    # use auto_now_add instead of auto_now as we want the timestamp to be fixed even if post is updated
    timestamp = models.DateTimeField(auto_now_add=True)
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)