

from bodzify_api.model.private.PrivateModel import PrivateModel
from bodzify_api.model.public_standard_resource.PublicStandardResource import PublicStandardResource
from bodzify_api.model.uuid.UuidModel import UuidModel


class PrivateUniqueResource(PrivateModel, UuidModel, PublicStandardResource):

    class Meta:
        abstract = True
