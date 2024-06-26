#!/usr/bin/env python

import os
from django.utils._os import safe_join
from django.utils.text import get_valid_filename

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from bodzify_api.settings import settings
from bodzify_api.validator.track_file_validator \
    import validate_size, validate_content_type_is_audio, validate_filename_length
import bodzify_api.utils.audio_metadata as audio_metadata


class ATTRIBUTES_LABEL:
    USER = 'user'
    FILE = 'file'
    FILENAME = 'filename'
    EXTENSION = 'extension'
    FINGERPRINT = "fingerprint"
    HAS_FINGERPRINT_GENERATION_FAILED = 'has_fingerprint_generation_failed'
    HAS_FLAC_MD5_BEEN_CORRECTED = 'has_flac_md5_been_corrected'
    SIZE_IN_BYTES = 'size_in_bytes'
    SIZE_IN_KO = 'size_in_ko'
    SIZE_IN_MO = 'size_in_mo'
    BITRATE_IN_KBPS = 'bitrate_in_kbps'


def _get_user_LIBRARIES_PATH(instance, filename):
    return '{0}{1}/{2}'.format(settings.LIBRARIES_DIR_NAME + '/' + settings.USER_LIBRARIES_DIR_NAME_PREFIXE,
                               instance.user.id,
                               filename)


LIBRARIES_PATH_MAX_LENGTH = len(
    settings.LIBRARIES_DIR_NAME) + len(settings.USER_LIBRARIES_DIR_NAME_PREFIXE) + len(settings.USER_MAX_NUMBER)
FILE_PATH_MAX_LENGTH = settings.LIB_TRACK_FILENAME_LEN_MAX + LIBRARIES_PATH_MAX_LENGTH


class PreserveSpacesStorage(FileSystemStorage):
    def get_valid_name(self, name):
        return name


class TrackFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    file = models.FileField(upload_to=_get_user_LIBRARIES_PATH,
                            storage=PreserveSpacesStorage(),
                            help_text="Only audio formats accepted.",
                            validators=[FileExtensionValidator(settings.LIB_TRACK_FILE_EXTENSIONS),
                                        validate_filename_length,
                                        validate_size,
                                        validate_content_type_is_audio],
                            max_length=FILE_PATH_MAX_LENGTH,
                            null=True)
    filename = models.CharField(max_length=settings.LIB_TRACK_FILENAME_LEN_MAX, blank=True)
    extension = models.CharField(max_length=5, blank=True)
    fingerprint = models.BinaryField(null=True, blank=True, default=None, editable=True)
    has_flac_md5_been_corrected = models.BooleanField(null=True, default=None, blank=True)
    size_in_bytes = models.DecimalField(null=True, blank=True, max_digits=11, decimal_places=2)
    size_in_ko = models.GeneratedField(expression=F(ATTRIBUTES_LABEL.SIZE_IN_BYTES) / 1024,  # type: ignore
                                       output_field=models.DecimalField(max_digits=8, decimal_places=2),
                                       db_persist=True)
    size_in_mo = models.GeneratedField(expression=F(ATTRIBUTES_LABEL.SIZE_IN_BYTES) / (1024 * 1024),  # type: ignore
                                       output_field=models.DecimalField(max_digits=5, decimal_places=2),
                                       db_persist=True)
    bitrate_in_kbps = models.IntegerField(null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now, editable=False)

    @property
    def has_fingerprint_generation_failed(self):
        return self.fingerprint is None

    class Meta:
        db_table = 'bodzify_api_track_file'
        verbose_name = 'Track File'
        verbose_name_plural = 'Track Files'

    def __str__(self) -> str:
        if self.file and self.file.name:
            return self.file.name + " (" + str(self.size_in_bytes) + " bytes)"
        return ""

    def save(self, *args, **kwargs):
        if self.file and self.file.name:
            self.filename = os.path.basename(self.file.name)
            self.extension = os.path.splitext(self.file.name)[1]
            self.size_in_bytes = self.file.size

        super().save(*args, **kwargs)  # So that the file is saved before eventual modifications

        self.bitrate_in_kbps = audio_metadata.get_bitrate_from_file(self.file.path)
        super().save(update_fields=[ATTRIBUTES_LABEL.BITRATE_IN_KBPS])

        if self.file and self.extension == '.flac':
            if not audio_metadata.is_flac_file_md5_valid(self.file.path):
                try:
                    audio_metadata.replace_flac_file_with_corrected_md5(self.file.path)
                    self.has_flac_md5_been_corrected = True
                except Exception:
                    raise ValidationError(
                        {ATTRIBUTES_LABEL.FILE: ["The Flac file md5 check failed and could not be corrected. The " +
                                                 "file is probably corrupted."]}
                    )
            else:
                self.has_flac_md5_been_corrected = False
            super().save(update_fields=[ATTRIBUTES_LABEL.HAS_FLAC_MD5_BEEN_CORRECTED])
