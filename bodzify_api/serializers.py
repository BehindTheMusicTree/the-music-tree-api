from django.contrib.auth.models import User, Group

from rest_framework import serializers

from bodzify_api.models import LibrarySong


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class LibrarySongSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibrarySong
        fields = [
            'uuid',
            'relativeUrl',
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