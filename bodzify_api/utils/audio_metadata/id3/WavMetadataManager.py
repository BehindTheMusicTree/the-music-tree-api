
import os
import wave
import tempfile

from mutagen._file import File as MutagenFile

from bodzify_api.utils.audio_metadata.id3.Id3Manager import Id3Manager


class WavMetadataManager(Id3Manager):

    def get_raw_metadata(self) -> dict:
        self.audio_file.seek(0)
        file_metadata = MutagenFile(self.audio_file)
        if file_metadata.tags is None:  # type: ignore
            file_metadata.add_tags()  # type: ignore
        return file_metadata.tags  # type: ignore
