from django.contrib.auth.models import User, Group

from rest_framework import serializers

from bodzify_api.models import LibraryTrack, Genre

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups']


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