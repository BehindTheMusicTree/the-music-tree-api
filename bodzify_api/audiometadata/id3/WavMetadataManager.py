#!/usr/bin/env python

from mutagen._file import File as MutagenFile
from mutagen._file import FileType as MutagenFileMetadata

from bodzify_api.audiometadata.id3.Id3Manager import Id3Manager


class WavMetadataManager(Id3Manager):

    def __init__(self, file):
        super().__init__(file)

    def _get_file_metadata(self) -> MutagenFileMetadata:
        file_metadata = MutagenFile(self.file)
        if file_metadata.tags is None:  # type: ignore
            file_metadata.add_tags()  # type: ignore
        return file_metadata.tags  # type: ignore
