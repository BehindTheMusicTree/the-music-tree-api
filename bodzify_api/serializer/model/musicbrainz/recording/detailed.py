from rest_framework import serializers

from bodzify_api.model.musicbrainz_resource.children.recording.MusicbrainzRecording import \
    Fields as ModelFields
from bodzify_api.model.musicbrainz_resource.children.recording.MusicbrainzRecording import \
    MusicbrainzRecording
from bodzify_api.serializer.model.musicbrainz.artist.detailed import \
    MusicbrainzArtistDetailedSerializer


class Fields:
    MUSICBRAINZ_ID = ModelFields.MUSICBRAINZ_ID
    TITLE = ModelFields.TITLE
    SCORE = ModelFields.SCORE
    MUSICBRAINZ_ARTISTS = ModelFields.MUSICBRAINZ_ARTISTS
    MUSICBRAINZ_LINK = ModelFields.MUSICBRAINZ_LINK
    DURATION_IN_SEC = ModelFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ModelFields.DURATION_STR_IN_HOUR_MIN_SEC
    RELEASE_DATE = ModelFields.RELEASE_DATE


class MusicbrainzRecordingDetailedSerializer(serializers.ModelSerializer):
    musicbrainz_artists = MusicbrainzArtistDetailedSerializer(many=True)

    class Meta:
        model = MusicbrainzRecording
        fields = [
            Fields.MUSICBRAINZ_ID,
            Fields.TITLE,
            Fields.SCORE,
            Fields.MUSICBRAINZ_ARTISTS,
            Fields.MUSICBRAINZ_LINK,
            Fields.DURATION_IN_SEC,
            Fields.DURATION_STR_IN_HOUR_MIN_SEC,
            Fields.RELEASE_DATE
        ]
