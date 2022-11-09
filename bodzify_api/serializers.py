from django.contrib.auth.models import User, Group

from rest_framework import serializers

from bodzify_api.models import LibraryTrack, MineTrack, Genre, Query

import logging

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

class GenreSerializer(serializers.ModelSerializer):
    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
            
    class Meta:
        model = Genre
        fields = ['uuid', 'name', 'parent', 'addedOn']

    def create(self, validatedGenre):
        validatedGenre['user'] = self._user()
        return Genre.objects.create(**validatedGenre)

class LibraryTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryTrack
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

class LibraryTrackResponseSerializer(serializers.ModelSerializer):
    genreName = serializers.SerializerMethodField()

    def get_genreName(self, obj):
        if obj.genre is None:
            return None
        return obj.genre.name

    class Meta:
        model = LibraryTrack
        fields = [
            'uuid',
            'relativeUrl',
            'filename',
            'fileExtension',
            "title", 
            "artist", 
            "album", 
            "genreName", 
            "duration", 
            "rating", 
            "language", 
            "addedOn"]

class MineTrackSerializer(serializers.Serializer):
    class Meta:
        model = MineTrack
        fields = [
            "title", 
            "artist", 
            "duration",
            "releasedOn",
            "url"]

class QuerySerializer(serializers.Serializer):
    class Meta:
        model = Query
        fields = ["query", "page", "pageNumber"]
