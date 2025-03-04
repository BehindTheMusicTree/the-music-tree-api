from bodzify_api.model.base.PolymorphicDynamicTableNameModelBase import PolymorphicDynamicTableNameModelBase
from bodzify_api.model.private.PrivateModel import PrivateModel
from bodzify_api.model.public_standard_resource.PublicStandardResource import PublicStandardResource


class PrivateStandardResource(PrivateModel, PublicStandardResource, metaclass=PolymorphicDynamicTableNameModelBase):
    """
    The metaclass=PolymorphicDynamicTableNameModelBase parameter serves two critical purposes:

    1. Polymorphic Behavior:
       - Enables polymorphic queries through the model hierarchy
       - Allows retrieving heterogeneous sets of objects with a single query
       - Maintains proper type information when loading objects from database

    2. Dynamic Table Names:
       - Instead of using a fixed database table for all instances
       - Table names are generated at runtime based on tenant/organization ID
       - Enables multi-tenancy with separate tables per client/organization
       - Provides data isolation between different tenants in the same database
    """
    class Meta:
        abstract = True
