from django.db.models import QuerySet

from bodzify_api.model.base.BaseQuerySet import BaseQuerySet


class PlaylistQuerySet(BaseQuerySet):

    def _get_queryset_str_filter_value_to_filter_nothing(self) -> str:
        """Returns a value that will match nothing when used in a __icontains queryset string filter."""
        return 'FILTER_NOTHING'
