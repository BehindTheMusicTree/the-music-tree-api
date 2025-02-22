
from bodzify_api.utils.audio_metadata.audio_file import AudioFile
import os
import wave
import tempfile

from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.db.models.fields.files import FieldFile
from mutagen._file import File as MutagenFile
from mutagen._file import FileType as MutagenFileMetadata

from bodzify_api.utils.audio_metadata.exceptions import FileTypeNotSupportedError
from bodzify_api.utils.audio_metadata.id3.Id3Manager import Id3Manager


class WavMetadataManager(Id3Manager):

    def __init__(self, audio_file: AudioFile):
        super().__init__(audio_file)
        self.audio_file = audio_file

    def get_raw_metadata(self) -> MutagenFileMetadata:
        self.audio_file.seek(0)
        file_metadata = MutagenFile(self.audio_file)
        if file_metadata.tags is None:  # type: ignore
            file_metadata.add_tags()  # type: ignore
        return file_metadata.tags  # type: ignore

    def get_bitrate(self):
        self.audio_file.seek(0)
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(self.audio_file.read())
            tmp.close()
            file_path = tmp.name

        # Open and process the WAV file
        wave_file = wave.open(file_path, 'rb')
        try:
            frames = wave_file.getnframes()
            rate = wave_file.getframerate()
            duration_in_sec = frames / float(rate)
            bitrate = os.path.getsize(file_path) * 8 / duration_in_sec / 1000
            return bitrate
        finally:
            wave_file.close()
            os.unlink(file_path)
