from mutagen._file import File as MutagenFile
from mutagen.flac import FLAC
from mutagen.id3 import ID3

from bodzify_api.utils.audio_metadata.id3.Id3Manager import Id3Manager


class FlacID3v2Manager(Id3Manager):
    def __init__(self, file, file_path):
        super().__init__(file, file_path)
        self.id3v2_metadata = self._extract_id3v2_metadata()
        self.flac_metadata = self._extract_flac_metadata()

    def _extract_id3v2_metadata(self):
        try:
            id3 = ID3(self.file)
            return id3
        except Exception:
            return None

    def _extract_flac_metadata(self):
        try:
            flac = FLAC(self.file)
            return flac
        except Exception:
            return None

    @property
    def file_metadata(self):
        if self.id3v2_metadata:
            return self.id3v2_metadata
        else:
            return self.flac_metadata

    def is_md5_valid(self):
        if self.id3v2_metadata:
            if self.flac_metadata:
                # Strip ID3v2 tag before calculating MD5 checksum
                self.flac_metadata.delete()
                return super().is_md5_valid()
            else:
                return False
        else:
            return super().is_md5_valid()
