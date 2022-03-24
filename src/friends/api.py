from django.http.response import HttpResponse
from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins

class FriendDetail(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    serializer_class = FriendListSerializer
    queryset = FriendList.objects.all()
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)