from typing import Optional

from django_filters import Filter
from bodzify_api.utils.validation_error_utils import raise_validation_error


class AppFilter(Filter):
    field_name_user_friendly: Optional[str]

    def __init__(self, field_name_user_friendly: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field_name_user_friendly = field_name_user_friendly

        if self.field_name and not self.field_name_user_friendly:
            raise_validation_error(
                message='field_name_user_friendly must be provided when field_name is set',
                code='missing_field_name_user_friendly',
                field='field_name_user_friendly'
            )
