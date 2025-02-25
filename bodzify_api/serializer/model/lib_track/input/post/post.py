
from bodzify_api.serializer.field.AppFileField import AppFileField
from bodzify_api.serializer.model.lib_track.input.input import \
    LibTrackInputSerializer
from bodzify_api.validator.TrackFileValidator import TrackFileValidator

from .Fields import Fields


class LibTrackPostSerializer(LibTrackInputSerializer):
    file = AppFileField(
        required=True,
        field_name=Fields.TRACK_FILE_PUBLIC,
        validators=[TrackFileValidator()],)
