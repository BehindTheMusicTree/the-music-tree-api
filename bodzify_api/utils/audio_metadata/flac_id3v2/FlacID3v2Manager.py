import logging
from typing import IO
from bodzify_api.utils.audio_metadata.audio_file import AudioFile
from mutagen._file import File as MutagenFile
from mutagen.flac import FLAC
from mutagen.id3 import ID3

from bodzify_api.utils.audio_metadata.id3.Id3Manager import Id3Manager


class FlacID3v2Manager(Id3Manager):
    """
    Manager class for handling FLAC files with ID3v2 tags.

    Args:
        file: A file-like object representing the FLAC file. It should support
              the `seek` and `read` methods.
    """
    logger = logging.getLogger(__name__)

    def __init__(self, audio_file: AudioFile):
        super(FlacID3v2Manager, self).__init__(audio_file)
        self.id3v2_metadata = self._extract_id3v2_metadata()

    def _extract_id3v2_metadata(self):
        try:
            id3 = ID3(self.audio_file)
            return id3
        except Exception as e:
            self.logger.error(f"Failed to extract ID3v2 metadata: {str(e)}")
            return None

    @property
    def file_metadata(self):
        return self.id3v2_metadata

    def is_md5_valid(self):
        if self.id3v2_metadata:
            # Strip ID3v2 tag before calculating MD5 checksum
            self.audio_file.seek(0)  # type: ignore
            audio_data = self.audio_file.read()  # type: ignore
            self.id3v2_metadata.delete(self.audio_file)
            return super(FlacID3v2Manager, self).is_md5_valid(audio_data)
        else:
            return False
