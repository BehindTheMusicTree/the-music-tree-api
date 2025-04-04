
from bodzify_api.model.lib_track.Fields import Fields
from bodzify_api.view.serializer.model.lib_track.simple import UploadedTrackSimpleSerializer


class UploadedTrackDetailedSerializer(UploadedTrackSimpleSerializer):
    class Meta(UploadedTrackSimpleSerializer.Meta):
        fields = UploadedTrackSimpleSerializer.Meta.fields + [
            Fields.FILE_PATH,
            Fields.USER,
        ]
