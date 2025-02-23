
from mutagen._file import File as MutagenFile
from mutagen.id3._util import ID3NoHeaderError
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4StreamInfoError

from bodzify_api.utils.audio_metadata.id3.Id3Manager import Id3Manager


class Mp3MetadataManager(Id3Manager):

    def get_raw_metadata(self) -> dict:
        try:
            return MutagenFile(self.audio_file)  # type: ignore
        except (ID3NoHeaderError, MP4StreamInfoError):
            return {}

    def get_bitrate(self):
        self.audio_file.seek(0)
        return MP3(self.audio_file).info.bitrate  # type: ignore
