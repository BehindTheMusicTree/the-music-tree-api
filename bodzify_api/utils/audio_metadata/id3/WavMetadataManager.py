
import os
import wave
import tempfile

from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.db.models.fields.files import FieldFile
from mutagen._file import File as MutagenFile
from mutagen._file import FileType as MutagenFileMetadata

from bodzify_api.utils.audio_metadata.id3.Id3Manager import Id3Manager


class WavMetadataManager(Id3Manager):

    def __init__(self, file):
        super().__init__(file)

    def get_raw_metadata(self) -> MutagenFileMetadata:
        file_metadata = MutagenFile(self.file)
        if file_metadata.tags is None:  # type: ignore
            file_metadata.add_tags()  # type: ignore
        return file_metadata.tags  # type: ignore

    def get_bitrate(self):
        # Handle different file types appropriately
        if isinstance(self.file, TemporaryUploadedFile):
            file_path = self.file.temporary_file_path()
        elif isinstance(self.file, FieldFile):
            file_path = self.file.path
        elif isinstance(self.file, InMemoryUploadedFile):
            # Create temporary file for in-memory uploads
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                for chunk in self.file.chunks():
                    tmp.write(chunk)
                tmp.close()
                file_path = tmp.name
        else:
            # Try to get the name for other file types
            if self.file.file:  # type: ignore
                file_path = self.file.file.name  # type: ignore
            else:
                file_path = self.file.name  # type: ignore

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
            # Clean up temporary file if we created one
            if isinstance(self.file, InMemoryUploadedFile):
                os.unlink(file_path)
