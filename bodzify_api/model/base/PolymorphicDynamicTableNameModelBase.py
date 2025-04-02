
from polymorphic.models import PolymorphicModelBase
from bodzify_api.model.base.DynamicTableNameModelBase import DynamicTableNameModelBase


class PolymorphicDynamicTableNameModelBase(PolymorphicModelBase, DynamicTableNameModelBase):
    pass
