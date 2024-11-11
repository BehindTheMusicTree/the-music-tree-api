from django.db import models


class PlaylistQuerySet(models.QuerySet):
    def _get_queryset_str_filter_value_to_filter_nothing(self):
        # Returns a value that will match nothing when used in a __icontains queryset string filter
        return 'FILTER_NOTHING'
