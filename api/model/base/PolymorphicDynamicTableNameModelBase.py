
from polymorphic.models import PolymorphicModelBase
from api.model.base.DynamicTableNameModelBase import DynamicTableNameModelBase


class PolymorphicDynamicTableNameModelBase(PolymorphicModelBase, DynamicTableNameModelBase):
    pass
