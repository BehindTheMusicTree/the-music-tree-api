#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.tag.Tag import Tag
from bodzify_api.serializer.tag.TagTypeSerializer import TagTypeSerializer 

class TagRequestSerializer(serializers.ModelSerializer):
            
    class Meta:
        model = Tag
        fields = ['uuid', 'name', 'parent']

class TagResponseSerializer(serializers.ModelSerializer):
                
    class Meta:
        model = Tag
        fields = ['uuid', 'name', 'parent', 'addedOn']