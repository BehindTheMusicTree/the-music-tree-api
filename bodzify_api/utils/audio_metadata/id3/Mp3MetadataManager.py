
from mutagen._file import File as MutagenFile
from mutagen._file import FileType as MutagenFileMetadata
from mutagen.id3 import ID3
from mutagen.id3._util import ID3NoHeaderError
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4StreamInfoError

from bodzify_api.utils.audio_metadata.id3.Id3Manager import Id3Manager
from bodzify_api.utils.audio_metadata.audio_file import AudioFile


class Mp3MetadataManager(Id3Manager):

    def __init__(self, audio_file: AudioFile):
        super().__init__(audio_file)
        self.audio_file = audio_file

    def get_raw_metadata(self) -> MutagenFileMetadata:
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
