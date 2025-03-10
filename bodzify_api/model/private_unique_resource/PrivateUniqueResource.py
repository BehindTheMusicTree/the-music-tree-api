import uuid

from django.db import models

from bodzify_api.model.private.PrivateModel import PrivateModel
from bodzify_api.model.public_standard_resource.PublicStandardResource import PublicStandardResource
from bodzify_api.model.uuid.UuidModel import UuidModel


class PrivateUniqueResource(PrivateModel, UuidModel, PublicStandardResource):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
