
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.model.playlist.children.manual.Fields import Fields as ModelFields
from bodzify_api.serializer.AppValidationSerializer import AppValidationSerializer


class ManualPlaylistInputSerializer(AppValidationSerializer, serializers.ModelSerializer):
    class Meta:
        model = ManualPlaylist
        fields = [ModelFields.NAME_PUBLIC]

    def validate(self, data):
        user = self.context['request'].user
        name = data.get(ModelFields.NAME_PUBLIC)  # Try to get from validated data first
        if name is None:  # If not in validated data
            name = self.initial_data.get('name')  # Get from initial data
            data[ModelFields.NAME_PUBLIC] = name  # Add to data dictionary
        if ManualPlaylist.objects.filter(user=user, name=name).exists():
            raise ValidationError({ModelFields.NAME_PUBLIC: "already exists"})
        return super().validate(data)
