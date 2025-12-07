from api.model.public_standard_resource.PublicStandardResource import PublicStandardResource
from api.model.uuid.UuidModel import UuidModel


class PublicUniqueResource(PublicStandardResource, UuidModel):

    class Meta:
        abstract = True
