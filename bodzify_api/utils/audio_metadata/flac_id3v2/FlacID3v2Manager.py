
from mutagen.id3 import ID3

from bodzify_api.utils.audio_metadata.id3.Id3Manager import Id3Manager


class FlacID3v2Manager(Id3Manager):

    def get_raw_metadata(self):
        return ID3(self.audio_file.file_path)
