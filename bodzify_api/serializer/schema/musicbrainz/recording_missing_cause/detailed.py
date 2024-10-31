
from rest_framework import serializers

from bodzify_api.model.musicbrainz.recording.missing_cause.MusicbrainzRecordingMissingCause \
    import MusicbrainzRecordingMissingCause, Fields as ModelFields


class Fields:
    CREATED_ON = ModelFields.CREATED_ON
    UPDATED_ON = ModelFields.UPDATED_ON
    CODE = ModelFields.CODE
    LABEL = ModelFields.MESSAGE


class MusicbrainzRecordingMissingCauseDetailedSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField(source=Fields.CODE)

    class Meta:
        model = MusicbrainzRecordingMissingCause
        fields = [Fields.CODE, Fields.LABEL]
