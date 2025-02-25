from rest_framework import serializers

from bodzify_api.model.track.file.flac.FlacTrackFile import FlacTrackFile
from bodzify_api.model.track.file.TrackFile import TrackFile
from bodzify_api.serializer.model.fingerprint_missing_cause.detailed import \
    FingerprintMissingCauseDetailedSerializer
from bodzify_api.serializer.model.musicbrainz.recording.detailed import \
    MusicbrainzRecordingDetailedSerializer

from .Fields import Fields
from .FlacSpecificFields import FlacSpecificFields


class FileDetailedSerializer(serializers.ModelSerializer):
    fingerprint_missing_cause = serializers.SerializerMethodField()
    musicbrainz_recording = MusicbrainzRecordingDetailedSerializer()
    musicbrainz_recording_missing_cause = serializers.SerializerMethodField()

    class Meta:
        model = TrackFile
        fields = [Fields.FILENAME,
                  Fields.EXTENSION,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.FINGERPRINT_MISSING_CAUSE,
                  Fields.SIZE_IN_BYTES,
                  Fields.SIZE_IN_KO,
                  Fields.SIZE_IN_MO,
                  Fields.BITRATE_IN_KBPS,
                  Fields.MUSICBRAINZ_RECORDING,
                  Fields.MUSICBRAINZ_RECORDING_MISSING_CAUSE,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if isinstance(instance, FlacTrackFile):
            data[FlacSpecificFields.ID3v2_TAGS_FOUND_AND_CONVERTED] = instance.id3v2_tags_found_and_converted
            data[FlacSpecificFields.MD5_HAS_BEEN_CORRECTED] = instance.md5_has_been_corrected
        return data

    def get_fingerprint_missing_cause(self, obj: TrackFile):
        if obj.fingerprint_memory is None:
            return FingerprintMissingCauseDetailedSerializer(obj.fingerprint_missing_cause).data
        return None

    def get_musicbrainz_recording_missing_cause(self, obj: TrackFile):
        if obj.musicbrainz_recording is None:
            return FingerprintMissingCauseDetailedSerializer(obj.musicbrainz_recording_missing_cause).data
        return None
