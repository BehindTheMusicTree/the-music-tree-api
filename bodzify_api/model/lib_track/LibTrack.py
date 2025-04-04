from django.db import models

from bodzify_api.model.base.BaseModel import BaseModel
from bodzify_api.model.field.AppCharField import AppCharField
from bodzify_api.model.lib_track.Fields import Fields
from bodzify_api.model.lib_track.LibTrackManager import LibTrackManager


class LibraryTrack(BaseModel):
    """Represents a track uploaded by a user to their library."""

    name = AppCharField(max_length=256, db_column=Fields.NAME)
    artist = AppCharField(max_length=256, null=True, db_column=Fields.ARTIST)
    album = AppCharField(max_length=256, null=True, db_column=Fields.ALBUM)
    genre = AppCharField(max_length=256, null=True, db_column=Fields.GENRE)
    tag = AppCharField(max_length=256, null=True, db_column=Fields.TAG)
    duration_ms = models.IntegerField(db_column=Fields.DURATION_MS)
    file_path = AppCharField(max_length=512, db_column=Fields.FILE_PATH)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, db_column=Fields.USER)

    objects = LibTrackManager()

    def __str__(self):
        return f"{self.name} - {self.artist or 'Unknown Artist'}"

    class Meta:
        db_table = 'lib_track'
        indexes = [
            models.Index(fields=[Fields.NAME]),
            models.Index(fields=[Fields.ARTIST]),
            models.Index(fields=[Fields.ALBUM]),
            models.Index(fields=[Fields.GENRE]),
            models.Index(fields=[Fields.TAG]),
            models.Index(fields=[Fields.USER]),
        ]
