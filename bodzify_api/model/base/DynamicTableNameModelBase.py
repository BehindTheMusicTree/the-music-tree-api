from django.db.models.base import ModelBase as DjangoModelBase

from bodzify_api import settings
from bodzify_api.utils.data_transformer import to_snake_case


class DynamicTableNameModelBase(DjangoModelBase):
    def __new__(cls, name, bases, attrs):
        dynamic_db_table_name = f"{settings.APP_NAME}_{to_snake_case(name)}"

        # TODO: I couldn't test if meta is abstract (where db_table should not be set).
        # if not hasattr(meta, 'db_table'):
        # TODO: Do not override if already set. Testing if set does not work as it is always set by the mother
        # abstract classes like BaseModel.

        meta = attrs.get('Meta', type('Meta', (), {}))
        meta.db_table = dynamic_db_table_name
        attrs['Meta'] = meta
        return super().__new__(cls, name, bases, attrs)
