#!/usr/bin/env python

from bodzify_api.model.base.utils.PrivateModel import PrivateModel, Fields as PrivateFields
from bodzify_api.model.base.PublicStandardResource import PublicStandardResource, Fields as PublicRelationFields


class Fields:
    CREATED_ON = PublicRelationFields.CREATED_ON
    UPDATED_ON = PublicRelationFields.UPDATED_ON
    USER = PrivateFields.USER


class PrivateStandardResource(PrivateModel, PublicStandardResource):

    class Meta:
        abstract = True
