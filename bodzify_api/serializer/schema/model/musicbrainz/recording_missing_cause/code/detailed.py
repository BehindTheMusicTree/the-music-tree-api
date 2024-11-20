
from rest_framework import serializers

from bodzify_api.model.musicbrainz_resource.children.recording.missing_cause.code.MusicbrainzRecordingMissingCauseCode \
    import MusicbrainzRecordingMissingCauseCode, Fields as ModelFields


class Fields:
    CODE = ModelFields.CODE
    LABEL = ModelFields.LABEL


class MusicbrainzRecordingMissingStandardCauseDetailedSerializer(serializers.ModelSerializer):

    class Meta:
        model = MusicbrainzRecordingMissingCauseCode
        fields = [Fields.CODE, Fields.LABEL]
