#!/usr/bin/env python
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.InputModelSerializer import InputModelSerializer


class CriteriaPostSerializer(InputModelSerializer):

    class Meta:
        model = Criteria
        fields = ['name', 'parent']
