from rest_framework import serializers
from .models import *

class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username','password']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username','date_joined','last_login']