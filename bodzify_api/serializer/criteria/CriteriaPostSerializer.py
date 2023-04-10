#!/usr/bin/env python
from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL
from bodzify_api.serializer.InputModelSerializer import InputModelSerializer


class CriteriaPostSerializer(InputModelSerializer):

    class Meta:
        model = Criteria
        fields = [ATTRIBUTES_LABEL.NAME, ATTRIBUTES_LABEL.PARENT]
