from typing import Optional

from django_filters import Filter


class AppFilter(Filter):
    field_name_user_friendly: Optional[str]

    def __init__(self, field_name_user_friendly: Optional[str] = None, *args, **kwargs):
        self.field_name_user_friendly = field_name_user_friendly
        super().__init__(*args, **kwargs)
