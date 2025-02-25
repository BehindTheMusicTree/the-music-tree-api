from bodzify_api.model.private.PrivateModel import PrivateModel
from bodzify_api.model.public_standard_resource.PublicStandardResource import \
    PublicStandardResource


class PrivateStandardResource(PrivateModel, PublicStandardResource):

    class Meta:
        abstract = True
