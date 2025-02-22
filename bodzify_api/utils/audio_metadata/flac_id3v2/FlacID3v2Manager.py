from mutagen._file import File as MutagenFile
from mutagen.flac import FLAC
from mutagen.id3 import ID3

from bodzify_api.utils.audio_metadata.id3.Id3Manager import Id3Manager


class FlacID3v2Manager(Id3Manager):
    def __init__(self, file, file_path):
        super().__init__(file, file_path)
        self.id3v2_metadata = self._extract_id3v2_metadata()

    def _extract_id3v2_metadata(self):
        try:
            id3 = ID3(self.file)
            return id3
        except Exception:
            return None

    @property
    def file_metadata(self):
        return self.id3v2_metadata

    def is_md5_valid(self):
        if self.id3v2_metadata:
            # Strip ID3v2 tag before calculating MD5 checksum
            with open(self.file_path, 'rb') as file:
                audio_data = file.read()
            self.id3v2_metadata.delete(self.file_path)
            return super().is_md5_valid(audio_data)
        else:
            return False
