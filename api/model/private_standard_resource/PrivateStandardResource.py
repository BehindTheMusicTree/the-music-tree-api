from api.model.private.PrivateModel import PrivateModel
from api.model.public_standard_resource.PublicStandardResource import PublicStandardResource


class PrivateStandardResource(PrivateModel, PublicStandardResource):

    class Meta:
        abstract = True
