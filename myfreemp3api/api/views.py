from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializers import *

from myfreemp3api.api.models import *
from myfreemp3api.api.controller import user_creation_controller
import myfreemp3api.api.configuration as api_cfg
from myfreemp3api.myfreemp3_scrapper import scrapper


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@csrf_exempt
@api_view(['POST'])
def UserCreationView(request):
    if (request.method == "POST"):
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        userId = user_creation_controller.CreateUser(name, email, password)
        return HttpResponseRedirect(str(userId))

@csrf_exempt
@api_view(['GET'])
def LoginView(request):
    if (request.method == "GET"):
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        userId = user_creation_controller.CreateUser(name, email, password)
        return HttpResponseRedirect(str(userId))

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def SongsView(request):
    if (request.method == "GET"):
        return JsonResponse(scrapper.scrap(request.GET.get("query", '')), safe = False)