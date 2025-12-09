from rest_framework import serializers

from api.model.uploaded_track.file.TrackFile import TrackFile
from api.serializer.model.musicbrainz.recording.detailed import MusicbrainzRecordingDetailedSerializer
from api.serializer.model.musicbrainz.recording_missing_cause.detailed import MusicbrainzRecordingMissingCauseDetailedSerializer

from .Fields import Fields


class FileDetailedSerializer(serializers.ModelSerializer):
    musicbrainz_recording = MusicbrainzRecordingDetailedSerializer()
    musicbrainz_recording_missing_cause = serializers.SerializerMethodField()

    class Meta:
        model = TrackFile
        fields = [Fields.FILENAME,
                  Fields.EXTENSION,
                  Fields.MD5_HAS_BEEN_CORRECTED,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.SIZE_IN_BYTES,
                  Fields.SIZE_IN_KO,
                  Fields.SIZE_IN_MO,
                  Fields.BITRATE_IN_KBPS,
                  Fields.MUSICBRAINZ_RECORDING,
                  Fields.MUSICBRAINZ_RECORDING_MISSING_CAUSE,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON]

    def get_musicbrainz_recording_missing_cause(self, obj: TrackFile):
        if obj.musicbrainz_recording is None:
            return MusicbrainzRecordingMissingCauseDetailedSerializer(obj.musicbrainz_recording_missing_cause).data
        return None
