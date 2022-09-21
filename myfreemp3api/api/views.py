from shutil import which
from .serializers import *

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
 
class SongsExternalView(APIView):
 
    def get(self, request):
        if request.GET.get('source', False) == "myfreemp3":
            return JsonResponse(scrapper.scrap(request.GET.get('query', False)), safe = False)
        else:
            return JsonResponse({'status':'false','message':"The specified source doesn\'t exist"}
            , status=500)

@csrf_exempt
@api_view(['POST'])
def UserCreationView(request):
    if (request.method == "POST"):
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        userId = user_creation_controller.CreateUser(name, email, password)
        return HttpResponseRedirect(str(userId))