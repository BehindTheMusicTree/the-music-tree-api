
from django.db.models import Case, CharField, Q, Value, When

from bodzify_api.filtering.filter.char.NonEmptiableCharFilter import NonEmptiableCharFilter
from bodzify_api.model.base.BaseQuerySet import BaseQuerySet
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.model.playlist.children.criteria.CriterialessPlaylistNames import CriterialessPlaylistNames


class CriteriaNameFilter(NonEmptiableCharFilter):

    def filter(self, qs: BaseQuerySet, value: str) -> BaseQuerySet:
        if not value:
            return super().filter(qs, value)

        value_lower = value.lower()

        # Check for special names (genreless/tagless)
        special_name = Case(
            When(type__pk=CriteriaTypePks.GENRE, then=Value(CriterialessPlaylistNames.GENRE)),
            When(type__pk=CriteriaTypePks.TAG, then=Value(CriterialessPlaylistNames.TAG)),
            output_field=CharField(),
        )

        # For playlists without criteria, filter by special name
        special_names_filter = Q(criteria__isnull=True) & Q(type__pk__in=[CriteriaTypePks.GENRE, CriteriaTypePks.TAG])

        # For playlists with criteria, filter by the criteria's name
        # Use a subquery to get the criteria name to avoid the OneToOneField lookup issue
        criteria_name_filter = Q(criteria__isnull=False) & Q(
            criteria__uuid__in=Criteria.objects.filter(_name__icontains=value).values('uuid'))

        # Annotate with special name and apply the combined filter
        return qs.annotate(
            special_name=special_name
        ).filter(
            (special_names_filter & Q(special_name__icontains=value_lower)) |
            criteria_name_filter
        )
