from rest_framework import serializers

from bodzify_api.models import Genre

class GenreSerializer(serializers.ModelSerializer):
            
    class Meta:
        model = Genre
        fields = ['uuid', 'name', 'parent', 'addedOn']

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user

    def create(self, validatedGenre):
        validatedGenre['user'] = self._user()
        return Genre.objects.create(**validatedGenre)