
from bodzify_api.filtering.filter.char.NonEmptiableCharFilter import NonEmptiableCharFilter
from bodzify_api.filtering.filter.foreign_key.ForeignKeyFilter import ForeignKeyFilter
from bodzify_api.filtering.set.AppFilterSet import AppFilterSet
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.children.criteria.Fields import Fields as ModelFields
from .Fields import Fields


class CriteriaPlaylistFilterSet(AppFilterSet):
    name = NonEmptiableCharFilter(field_name=f'{ModelFields.CRITERIA}__{ModelFields.NAME}',
                                  field_name_user_friendly=Fields.NAME_PUBLIC,
                                  lookup_expr="icontains")
    parent = ForeignKeyFilter()

    class Meta:
        model = CriteriaPlaylist
        fields = [Fields.NAME_PUBLIC, Fields.PARENT]
