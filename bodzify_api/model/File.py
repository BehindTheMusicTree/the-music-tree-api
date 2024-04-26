#!/usr/bin/env python

import os
import subprocess

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

from bodzify_api import settings
from bodzify_api.validator.track_file_validator \
    import validate_size, validate_content_type_is_audio, validate_filename_length


class ATTRIBUTES_LABEL:
    FILE = 'file'
    FILENAME = 'filename'
    EXTENSION = 'extension'
    ORIGINAL_FLAC_FILE_MD5_CHECK_IS_VALID = 'original_flac_file_md5_check_is_valid'
    SIZE_IN_BYTES = 'size_in_bytes'
    SIZE_IN_KO = 'size_in_ko'
    SIZE_IN_MO = 'size_in_mo'


def _get_user_directory_path(instance, filename):
    return '{0}{1}/{2}'.format(settings.LIB_DIR_NAME + '/' + settings.USER_LIB_DIR_NAME_PREFIXE,
                               instance.user.id,
                               filename)


class PreserveSpacesStorage(FileSystemStorage):
    def get_valid_name(self, name):
        return name


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    file = models.FileField(upload_to=_get_user_directory_path,
                            storage=PreserveSpacesStorage(),
                            help_text="Only audio formats accepted.",
                            validators=[FileExtensionValidator(settings.LIB_TRACK_FILE_EXTENSIONS),
                                        validate_filename_length,
                                        validate_size,
                                        validate_content_type_is_audio],
                            null=True)
    filename = models.CharField(max_length=settings.LIB_TRACK_FILENAME_LENGTH_MAX, blank=True)
    extension = models.CharField(max_length=5, blank=True)
    original_flac_file_md5_check_is_valid = models.BooleanField(null=True, default=None, blank=True)
    size_in_bytes = models.FloatField(null=True, blank=True)
    size_in_ko = models.GeneratedField(expression=F(ATTRIBUTES_LABEL.SIZE_IN_BYTES) / 1024,
                                       output_field=models.FloatField(),
                                       db_persist=True)
    size_in_mo = models.GeneratedField(expression=F(ATTRIBUTES_LABEL.SIZE_IN_BYTES) / (1024 * 1024),
                                       output_field=models.FloatField(),
                                       db_persist=True)

    @staticmethod
    def is_flac_file_md5_valid(file_path):
        result = subprocess.run(['flac', '-t', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return 'ok' in result.stderr.decode()

    def __str__(self) -> str:
        if self.file and self.file.name:
            return self.file.name + " (" + str(self.size_in_bytes) + " bytes)"
        return ""

    def save(self, *args, **kwargs):
        if self.file and self.file.name:
            self.filename = os.path.basename(self.file.name)
            self.extension = os.path.splitext(self.file.name)[1]
            self.size_in_bytes = self.file.size

            if self.extension == '.flac':
                self.original_flac_file_md5_check_is_valid = self.is_flac_file_md5_valid(self.file.path)

        super().save(*args, **kwargs)
