from typing import Optional

from django.core.exceptions import ImproperlyConfigured
from django_filters import Filter


class AppFilter(Filter):
    field_name_user_friendly: Optional[str]

    def __init__(self, field_name_user_friendly: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field_name_user_friendly = field_name_user_friendly

        if self.field_name and not self.field_name_user_friendly:
            raise ImproperlyConfigured(
                'field_name_user_friendly must be provided when field_name is set'
            )
