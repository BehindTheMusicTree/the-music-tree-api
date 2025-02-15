from bodzify_api.model.artist.Artist import Artist
from bodzify_api.serializer.AppModelSerializer import AppModelSerializer
from bodzify_api.serializer.schema.model.album.Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME


class ArtistMinimumSerializer(AppModelSerializer):

    class Meta:
        model = Artist
        fields = [Fields.UUID, Fields.NAME]
