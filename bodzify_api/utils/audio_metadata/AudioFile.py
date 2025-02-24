
import os
import subprocess
import tempfile
from typing import Optional, Union
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.flac import FLAC

from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
from django.db.models.fields.files import FieldFile
from django.core.files import File as DjangoFile
from django.core.exceptions import ImproperlyConfigured

from bodzify_api.utils.audio_metadata.exceptions import FileCorruptedError


class AudioFile:

    file: TemporaryUploadedFile | FieldFile | InMemoryUploadedFile | str
    file_path: Optional[str]

    def __init__(self, file: Union[TemporaryUploadedFile, FieldFile, InMemoryUploadedFile, str]):

        if isinstance(file, FieldFile):
            file = file.file

        self.file = file

        if isinstance(file, TemporaryUploadedFile):
            self.file_path = file.temporary_file_path()
        elif isinstance(file, InMemoryUploadedFile):
            self.file_path = None
        elif isinstance(file, DjangoFile):
            self.file_path = file.name
        else:
            self.file_path = file

        if self.file_path is not None and not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File {self.file_path} does not exist")

        file_extension = os.path.splitext(
            self.file.name if isinstance(self.file, (TemporaryUploadedFile, FieldFile, InMemoryUploadedFile))
            else self.file if isinstance(self.file, str)
            else str(self.file)
        )[1].lower()
        self.file_extension = file_extension
        return

    def get_duration(self) -> float:
        path = self.get_file_path_or_object()
        if self.file_extension == '.mp3':
            audio = MP3(path)
            return audio.info.length
        elif self.file_extension == '.wav':
            audio = WAVE(path)
            return audio.info.length
        elif self.file_extension == '.flac':
            audio = FLAC(path)
            return audio.info.length
        else:
            raise NotImplementedError(f"Reading is not supported for file type: {type(self.file)}")

    def get_bitrate(self) -> int:
        path = self.get_file_path_or_object()
        if self.file_extension == '.mp3':
            audio = MP3(path)
            # Calculate MP3 bitrate from file size and duration
            if audio.info.length > 0 and isinstance(path, str) and os.path.exists(path):
                file_size = os.path.getsize(path)
                return int((file_size * 8) / self.get_duration() / 1000)
            return 0
        elif self.file_extension == '.wav':
            audio = WAVE(path)
            # WAV bitrate = sample_rate * channels * bits_per_sample
            return (audio.info.sample_rate * audio.info.channels *
                    audio.info.bits_per_sample) // 1000
        elif self.file_extension == '.flac':
            audio = FLAC(path)
            # FLAC bitrate = sample_rate * channels * bits_per_sample
            return (audio.info.sample_rate * audio.info.channels *
                    audio.info.bits_per_sample) // 1000
        else:
            raise NotImplementedError(f"Reading is not supported for file type: {type(self.file)}")

    def read(self, size: int = -1) -> bytes:
        if isinstance(self.file, InMemoryUploadedFile):
            return self.file.read(size)
        elif self.file_path is not None:
            with open(self.file_path, 'rb') as f:
                return f.read(size)
        else:
            raise NotImplementedError(f"Reading is not supported for file type: {type(self.file)}")

    def write(self, data: bytes) -> int:
        if isinstance(self.file, InMemoryUploadedFile):
            return self.file.write(data)
        elif self.file_path is not None:
            with open(self.file_path, 'wb') as f:
                return f.write(data)
        else:
            raise NotImplementedError(f"Writing is not supported for file type: {type(self.file)}")

    def seek(self, offset: int, whence: int = 0) -> int:
        if isinstance(self.file, InMemoryUploadedFile):
            # For InMemoryUploadedFile, we can directly use the file object
            return self.file.seek(offset, whence)
        elif self.file_path is not None:
            with open(self.file_path, 'rb') as f:
                return f.seek(offset, whence)
        else:
            raise NotImplementedError(f"Seeking is not supported for file type: {type(self.file)}")

    def close(self) -> None:
        if isinstance(self.file, (TemporaryUploadedFile, FieldFile, InMemoryUploadedFile)):
            self.file.close()
        else:
            raise NotImplementedError(f"Closing is not supported for file type: {type(self.file)}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_file_path_or_object(self):
        if isinstance(self.file, (InMemoryUploadedFile)):
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            for chunk in self.file.chunks():
                temp_file.write(chunk)
            temp_file.close()
            return temp_file.name
        else:
            return self.file_path

    def get_file_name(self):
        if isinstance(self.file, (TemporaryUploadedFile, FieldFile, InMemoryUploadedFile, DjangoFile)):
            return self.file.name
        elif isinstance(self.file, str):
            return self.file
        else:
            raise NotImplementedError(f"Reading is not supported for file type: {type(self.file)}")

    def is_flac_file_md5_valid(self) -> bool:
        if not self.file_extension == '.flac':
            raise ImproperlyConfigured("The file is not a FLAC file")

        if isinstance(self.file, InMemoryUploadedFile):
            self.file.seek(0)
            result = subprocess.run(
                ['flac', '-t', '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=self.read())
        else:
            # Then the file path is not None
            file_path: str = self.file_path  # type: ignore
            result = subprocess.run(['flac', '-t', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output = result.stderr.decode()
        if 'ok' in output:
            return True
        if 'MD5 signature mismatch' in output:
            return False
        else:
            raise Exception("The Flac file md5 check failed")

    def replace_flac_with_corrected_md5(self):
        # Create a temporary file to store the corrected FLAC content
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name

        if isinstance(self.file, InMemoryUploadedFile):
            self.file.seek(0)
            result = subprocess.run(
                ['flac', '-f', '--best', '-o', temp_path, '-'],
                input=self.read(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        else:
            # The file path is not None
            file_path: str = self.file_path  # type: ignore
            result = subprocess.run(
                ['flac', '-f', '--best', '-o', temp_path, '-'],
                input=file_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

        stderr = result.stderr.decode()
        if 'wrote' not in stderr:
            raise FileCorruptedError(
                "The Flac file md5 check failed and could not be corrected. The file is probably corrupted.")

        # Replace original file content with corrected content
        if isinstance(self.file, InMemoryUploadedFile):
            self.seek(0)
            with open(temp_path, 'rb') as f:
                self.write(f.read())
        else:
            # Path is not None
            file_path: str = self.file_path  # type: ignore
            with open(file_path, 'wb') as f, open(temp_path, 'rb') as temp_f:
                f.write(temp_f.read())

        # Clean up temporary file
        os.unlink(temp_path)
