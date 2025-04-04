
from bodzify_api.model.uploaded_track.Fields import Fields
from bodzify_api.view.serializer.model.uploaded_track.simple import UploadedTrackSimpleSerializer


class UploadedTrackDetailedSerializer(UploadedTrackSimpleSerializer):
    class Meta(UploadedTrackSimpleSerializer.Meta):
        fields = UploadedTrackSimpleSerializer.Meta.fields + [
            Fields.UUID,
            Fields.RELATIVE_URL,
            Fields.TITLE,
            Fields.FILE,
            Fields.ARTISTS,
            Fields.ALBUM,
            Fields.TRACK_NUMBER,
            Fields.GENRE,
            Fields.RATING,
            Fields.LANGUAGE,
            Fields.PLAYLISTS_PUBLIC,
            Fields.PLAY_COUNT,
            Fields.ARCHIVED,
            Fields.CREATED_ON,
            Fields.UPDATED_ON,]
