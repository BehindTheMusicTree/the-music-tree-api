from polymorphic.models import PolymorphicModelBase
from bodzify_api.model.private.PrivateModel import PrivateModel
from bodzify_api.model.public_standard_resource.PublicStandardResource import PublicStandardResource
from bodzify_api.model.base.DynamicTableNameModelBase import DynamicTableNameModelBase


class PolymorphicDynamicTableNameModelBase(PolymorphicModelBase, DynamicTableNameModelBase):
    pass


class PrivateStandardResource(PrivateModel, PublicStandardResource, metaclass=PolymorphicDynamicTableNameModelBase):

    class Meta:
        abstract = True
