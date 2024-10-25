#!/usr/bin/env python

from bodzify_api.model.base.PublicStandardResource import PublicStandardResource, Fields as PublicRelationFields
from bodzify_api.model.base.utils.UuidModel import UuidModel, Fields as UuidFields


class Fields:
    CREATED_ON = PublicRelationFields.CREATED_ON
    UPDATED_ON = PublicRelationFields.UPDATED_ON
    UUID = UuidFields.UUID


class PublicUniqueResource(PublicStandardResource, UuidModel):

    class Meta:
        abstract = True
