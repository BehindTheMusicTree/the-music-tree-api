from django.contrib.auth.models import User, Group
from rest_framework import serializers

from myfreemp3api.models import SongDB


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class SongDBSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SongDB
        fields = [
            "id", 
            "title", 
            "artist", 
            "album", 
            "genre", 
            "duration", 
            "rating", 
            "language", 
            "added_on"]