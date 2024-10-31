
from rest_framework import serializers
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack, Fields as ModelFields
from bodzify_api.model.track.file.TrackFile import TrackFile, Fields as TrackFileFields


class Fields:
    USER = ModelFields.USER
    TITLE = ModelFields.TITLE
    FILE = ModelFields.TRACK_FILE_USER_FRIENDLY
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = ModelFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE
    ARTISTS = ModelFields.ARTISTS
    ALBUM = ModelFields.ALBUM
    POSITION_IN_ALBUM = ModelFields.POSITION_IN_ALBUM
    GENRE = ModelFields.GENRE
    RATING = ModelFields.RATING
    LANGUAGE = ModelFields.LANGUAGE
    ARCHIVED = ModelFields.ARCHIVED


class TrackModelSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False)

    class Meta:
        model = LibraryTrack
        fields = [Fields.USER,
                  Fields.TITLE,
                  Fields.FILE,
                  Fields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE,
                  Fields.ARTISTS,
                  Fields.ALBUM,
                  Fields.POSITION_IN_ALBUM,
                  Fields.GENRE,
                  Fields.RATING,
                  Fields.LANGUAGE,
                  Fields.ARCHIVED]

    def save(self, **kwargs):
        # django_file = self.context['request'].data.get(Fields.FILE)

        validated_data: dict = self.validated_data  # type: ignore
        track_file_data = {
            TrackFileFields.USER: validated_data[Fields.USER],
            TrackFileFields.FILE: validated_data[Fields.FILE],
        }

        library_track_data = validated_data.copy()
        library_track_data.pop(Fields.FILE, None)

        library_track: LibraryTrack = LibraryTrack.objects.create_with_track_file(
            track_file_data=track_file_data,
            library_track_data=library_track_data
        )

        return library_track
