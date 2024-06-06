#!/usr/bin/env python

from mutagen.mp4 import MP4StreamInfoError
from mutagen.mp3 import MP3
from mutagen._file import File as MutagenFile
from mutagen._file import FileType as MutagenFileMetadata
from mutagen.id3 import ID3
from mutagen.id3._util import ID3NoHeaderError

from django.db.models.fields.files import FieldFile

from bodzify_api.utils.audio_metadata.id3.Id3Manager import Id3Manager


class Mp3MetadataManager(Id3Manager):

    def __init__(self, file):
        super().__init__(file)

    def _get_file_metadata(self) -> MutagenFileMetadata:
        if isinstance(self.file, FieldFile):
            tags = MP3(self.file).tags
        else:
            try:
                tags = MutagenFile(self.file)
            except (ID3NoHeaderError, MP4StreamInfoError):
                tags = None

        if tags is None:
            return ID3()  # type: ignore
        return tags

    def get_bitrate(self):
        return self.file_metadata.info.bitrate / 1000  # type: ignore
