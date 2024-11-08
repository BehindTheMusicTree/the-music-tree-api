from bodzify_api.model.uuid.UuidModel import UuidModel
from bodzify_api.model.public_standard_resource.PublicStandardResource import PublicStandardResource


class PublicUniqueResource(PublicStandardResource, UuidModel):

    class Meta:
        abstract = True
