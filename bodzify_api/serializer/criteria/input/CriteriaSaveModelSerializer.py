#!/usr/bin/env python

from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL
from rest_framework import serializers


class CriteriaSaveModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = [
            ATTRIBUTES_LABEL.USER,
            ATTRIBUTES_LABEL.NAME,
            ATTRIBUTES_LABEL.PARENT,
            ATTRIBUTES_LABEL.TYPE
        ]
