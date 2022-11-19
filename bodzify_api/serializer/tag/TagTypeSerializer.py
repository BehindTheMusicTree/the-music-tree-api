#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.tag.TagType import TagType

class TagTypeSerializer(serializers.ModelSerializer):
           
    class Meta:
        model = TagType
        fields = ['label']