
from api.filtering.filter.char.CriteriaNameFilter import CriteriaNameFilter
from api.filtering.filter.foreign_key.ForeignKeyFilter import ForeignKeyFilter
from api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet import PrivateUniqueResourceFilterSet
from api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from api.model.playlist.children.criteria.Fields import Fields as ModelFields

from .Fields import Fields


class CriteriaPlaylistFilterSet(PrivateUniqueResourceFilterSet):
    name = CriteriaNameFilter(field_name=f'{ModelFields.CRITERIA}__{ModelFields.NAME}',
                              field_name_public=Fields.NAME_PUBLIC,
                              lookup_expr="icontains")
    parent = ForeignKeyFilter()

    class Meta:
        model = CriteriaPlaylist
        fields = [Fields.NAME_PUBLIC, Fields.PARENT, *PrivateUniqueResourceFilterSet.get_date_fields()]
