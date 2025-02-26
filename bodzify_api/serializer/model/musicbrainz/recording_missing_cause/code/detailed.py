
from rest_framework import serializers

from bodzify_api.model.musicbrainz_resource.children.recording.missing_cause.code.MbRecordingMissingCauseCode import (
    Fields as ModelFields
)
from bodzify_api.model.musicbrainz_resource.children.recording.missing_cause.code.MbRecordingMissingCauseCode import (
    MbRecordingMissingCauseCode
)


class Fields:
    CODE = ModelFields.CODE
    LABEL = ModelFields.LABEL


class MusicbrainzRecordingMissingStandardCauseDetailedSerializer(serializers.ModelSerializer):

    class Meta:
        model = MbRecordingMissingCauseCode
        fields = [Fields.CODE, Fields.LABEL]
