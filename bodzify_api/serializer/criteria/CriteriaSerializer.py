#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.criteria.CriteriaTypeSerializer import CriteriaTypeSerializer 

class CriteriaRequestSerializer(serializers.ModelSerializer):
            
    class Meta:
        model = Criteria
        fields = ['uuid', 'name', 'parent']

class CriteriaResponseSerializer(serializers.ModelSerializer):
                
    class Meta:
        type = CriteriaTypeSerializer()
        model = Criteria
        fields = ['uuid', 'name', 'parent', 'type', 'addedOn']