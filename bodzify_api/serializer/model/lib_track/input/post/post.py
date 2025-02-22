from bodzify_api.serializer.model.lib_track.input.input import LibTrackInputSerializer
from bodzify_api.validator.track_file_validator import FileExtensionValidator
from bodzify_api.serializer.field.AppFileField import AppFileField
from .Fields import Fields


class LibTrackPostSerializer(LibTrackInputSerializer):
    file = AppFileField(
        required=True,
        field_name=Fields.TRACK_FILE_PUBLIC,
        validators=[
            FileExtensionValidator(allowed_extensions=['wav', 'mp3', 'flac'])])
