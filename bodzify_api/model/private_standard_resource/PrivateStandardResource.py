from polymorphic.models import PolymorphicModelBase
from bodzify_api.model.private.PrivateModel import PrivateModel
from bodzify_api.model.public_standard_resource.PublicStandardResource import PublicStandardResource
from bodzify_api.model.base.DynamicTableNameModelBase import DynamicTableNameModelBase
from bodzify_api.model.base.PolymorphicBaseManager import PolymorphicBaseManager


class PolymorphicDynamicTableNameModelBase(PolymorphicModelBase, DynamicTableNameModelBase):
    """
    Metaclass that combines PolymorphicModelBase and DynamicTableNameModelBase.
    Sets PolymorphicBaseManager as the default manager for polymorphic models.
    """
    def __new__(cls, name, bases, attrs):
        # Set PolymorphicBaseManager as the default manager if not explicitly set
        if 'objects' not in attrs:
            attrs['objects'] = PolymorphicBaseManager()

        return super().__new__(cls, name, bases, attrs)


class PrivateStandardResource(PrivateModel, PublicStandardResource, metaclass=PolymorphicDynamicTableNameModelBase):

    class Meta:
        abstract = True
