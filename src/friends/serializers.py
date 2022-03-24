from rest_framework import serializers
from .models import *
from users.serializers import *

class FriendListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    friends = UserSerializer(many=True)
    class Meta:
        model = FriendList
        fields = ['user','friends']