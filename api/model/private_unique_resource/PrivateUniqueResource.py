

from api.model.private.PrivateModel import PrivateModel
from api.model.public_standard_resource.PublicStandardResource import PublicStandardResource
from api.model.uuid.UuidModel import UuidModel


class PrivateUniqueResource(PrivateModel, UuidModel, PublicStandardResource):

    class Meta:
        abstract = True
