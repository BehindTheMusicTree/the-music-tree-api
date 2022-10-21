from django.contrib.auth.models import User, Group
from rest_framework import serializers

from myfreemp3api.models import SongDB


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class SongDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongDB
        fields = [
            'uuid',
            'filename',
            'fileExtension',
            "title", 
            "artist", 
            "album", 
            "genre", 
            "duration", 
            "rating", 
            "language", 
            "addedOn"]