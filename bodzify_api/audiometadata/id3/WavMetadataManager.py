#!/usr/bin/env python

from typing import Optional
from mutagen.mp4 import MP4StreamInfoError
from mutagen.mp3 import MP3
from mutagen._file import File as MutagenFile
from mutagen.id3 import ID3
from mutagen.id3._util import ID3NoHeaderError
from mutagen.id3._frames import POPM, TALB, TCON, TIT2, TLAN, TPE1, TPE2
from mutagen.wave import WAVE

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models.fields.files import FieldFile
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from bodzify_api.audiometadata.MetadataManager import MetadataManager
from bodzify_api.audiometadata.id3.Id3Manager import Id3Manager


class WavMetadataManager(Id3Manager):

    def __init__(self, file):
        super().__init__(file)

    def _get_file_metadata(self):
        mutagen_wave_file = WAVE()
        mutagen_wave_file.add_tags()
        return mutagen_wave_file.tags
