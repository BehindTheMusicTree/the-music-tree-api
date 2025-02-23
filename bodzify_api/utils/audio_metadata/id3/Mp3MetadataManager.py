
from mutagen._file import File as MutagenFile
from mutagen.id3 import ID3
from mutagen.id3._util import ID3NoHeaderError
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4StreamInfoError

from bodzify_api.utils.audio_metadata.id3.Id3Manager import Id3Manager
from bodzify_api.utils.audio_metadata.audio_file import AudioFile


class Mp3MetadataManager(Id3Manager):

    def get_raw_metadata(self) -> dict:
        try:
            tags = MutagenFile(self.audio_file)
        except (ID3NoHeaderError, MP4StreamInfoError):
            tags = None

        if tags is None:
            return ID3()  # type: ignore
        return tags

    def get_bitrate(self):
        self.audio_file.seek(0)
        return MP3(self.audio_file).info.bitrate
