#!/usr/bin/env python

from bodzify_api.model.criteria.Criteria import Criteria, AttributesLabel
from rest_framework import serializers


class CriteriaModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = [AttributesLabel.USER,
                  AttributesLabel.NAME,
                  AttributesLabel.PARENT,
                  AttributesLabel.TYPE]
