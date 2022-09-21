from ..serializers import *

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from myfreemp3api.api.models import *
from myfreemp3api.api.controller import user_creation_controller
from myfreemp3api.myfreemp3_scrapper import scrapper

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
 
class SongDownloadView(APIView):
 
    def get(self, request):
        return JsonResponse(scrapper.scrap(request.query_params["query"]), safe = False)

@csrf_exempt
@api_view(['POST'])
def UserCreationView(request):
    if (request.method == "POST"):
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        userId = user_creation_controller.CreateUser(name, email, password)
        return HttpResponseRedirect(str(userId))