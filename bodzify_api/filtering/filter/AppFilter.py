
from django.core.exceptions import ImproperlyConfigured
from django_filters import Filter


class AppFilter(Filter):
    field_name_public: str | None

    def __init__(self, field_name_public: str | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field_name_public = field_name_public

        if self.field_name and not self.field_name_public:
            raise ImproperlyConfigured('field_name_public must be provided when field_name is set')
