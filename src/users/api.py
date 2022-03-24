from django.http.response import HttpResponse
from .forms import *
from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins

class CreateUser(mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreationSerializer
    form_class = UserRegistrationForm

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class UserDetail(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)