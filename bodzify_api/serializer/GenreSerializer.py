from rest_framework import serializers

from django.db.models import Count

from bodzify_api.models import Genre
import logging

class GenreRequestSerializer(serializers.ModelSerializer):
            
    class Meta:
        model = Genre
        fields = ['uuid', 'name', 'parent', 'addedOn']

class GenreResponseSerializer(serializers.ModelSerializer):
            
    trackCount = serializers.IntegerField(source='librarytrack_set.count')    
    
    class Meta:
        model = Genre
        fields = ['uuid', 'user', 'name', 'parent', 'addedOn', 'trackCount']