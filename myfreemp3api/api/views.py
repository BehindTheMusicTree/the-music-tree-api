from django.contrib.auth.models import User, Group
from myfreemp3api.api.models import *
from rest_framework import viewsets
from .serializers import *
from django.http import JsonResponse
from myfreemp3api.myfreemp3_scrapper import scrapper

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

def SongView(request):
    if (request.method == "GET"):
        return JsonResponse(scrapper.scrap(request.GET.get('search', '')), safe=False)