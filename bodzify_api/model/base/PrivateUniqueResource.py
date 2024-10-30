#!/usr/bin/env python

import uuid
from django.db import models

from bodzify_api.model.base.utils.PrivateModel import PrivateModel, Fields as PrivateFields
from bodzify_api.model.base.utils.public_standard_resource.PublicStandardResource import PublicStandardResource, Fields as PublicRelationFields
from bodzify_api.model.base.utils.UuidModel import UuidModel, Fields as UuidFields


class Fields:
    CREATED_ON = PublicRelationFields.CREATED_ON
    UPDATED_ON = PublicRelationFields.UPDATED_ON
    USER = PrivateFields.USER
    UUID = UuidFields.UUID


class PrivateUniqueResource(PrivateModel, UuidModel, PublicStandardResource):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
