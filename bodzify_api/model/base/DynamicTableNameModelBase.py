from django.db.models.base import ModelBase as DjangoModelBase

from bodzify_api import settings
from bodzify_api.utils.data_transformer import to_snake_case
from bodzify_api.utils.utils import print_django


class DynamicTableNameModelBase(DjangoModelBase):
    def __new__(cls, name, bases, attrs):
        dynamic_db_table_name = f"{settings.APP_NAME}_{to_snake_case(name)}"

        # TODO: I couldn't test if meta is abstract (where db_table should not be set).
        # if not hasattr(meta, 'db_table'):
        # TODO: Do not override if already set. Testing if set does not work as it is always set by the mother
        # abstract classes like BaseModel.

        meta = attrs.get('Meta', type('Meta', (), {}))
        if hasattr(meta, 'abstract'):
            if meta.abstract:
                print_django(f"{name} is abstract. Skipping dynamic table name setting.")
                return super().__new__(cls, name, bases, attrs)
        print_django(f"{name} is not abstract. Setting dynamic table name to {dynamic_db_table_name}.")

        meta.db_table = dynamic_db_table_name
        attrs['Meta'] = meta
        return super().__new__(cls, name, bases, attrs)
