from django_filters import CharFilter

from api.filtering.filter.char.EmptiableCharFilter import EmptiableCharFilter
from api.filtering.filter.char.RelatedObjectCharFilter import RelatedObjectCharFilter
from api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet import (
    PrivateUniqueResourceFilterSet
)
from api.model.album.Fields import Fields as AlbumFields
from api.model.artist.Fields import Fields as ArtistFields
from api.model.criteria.Criteria import Fields as CriteriaFields
from api.model.uploaded_track.Fields import Fields as ModelFields
from api.model.uploaded_track.UploadedTrack import UploadedTrack

from .Fields import Fields


class UploadedTrackFilterSet(PrivateUniqueResourceFilterSet):
    title = CharFilter(field_name=ModelFields.TITLE, lookup_expr='icontains')
    artists_name = RelatedObjectCharFilter(primary_field=ArtistFields.NAME_INTERNAL,
                                           field_name=ModelFields.ARTISTS,
                                           field_name_public=Fields.ARTISTS_NAME,
                                           lookup_expr='icontains')

    album_name = RelatedObjectCharFilter(primary_field=AlbumFields.NAME_INTERNAL,
                                         field_name=ModelFields.ALBUM,
                                         field_name_public=Fields.ALBUM_NAME,
                                         lookup_expr='icontains')

    genre_name = RelatedObjectCharFilter(primary_field=CriteriaFields.NAME_INTERNAL,
                                         field_name=ModelFields.GENRE,
                                         field_name_public=Fields.GENRE_NAME,
                                         lookup_expr='icontains')
    language = EmptiableCharFilter(
        field_name_public=ModelFields.LANGUAGE, field_name=ModelFields.LANGUAGE, lookup_expr='icontains')

    class Meta:
        model = UploadedTrack
        fields = [
            Fields.TITLE,
            Fields.LANGUAGE,
            *PrivateUniqueResourceFilterSet.get_date_fields()
        ]
