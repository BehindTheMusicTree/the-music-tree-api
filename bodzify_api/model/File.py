#!/usr/bin/env python

import os
import subprocess
from sys import stderr

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from bodzify_api import settings
from bodzify_api.validator.track_file_validator \
    import validate_size, validate_content_type_is_audio, validate_filename_length


class ATTRIBUTES_LABEL:
    USER = 'user'
    FILE = 'file'
    FILENAME = 'filename'
    EXTENSION = 'extension'
    HAD_FLAC_MD5_BEEN_CORRECTED = 'had_flac_md5_been_corrected'
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
    had_flac_md5_been_corrected = models.BooleanField(null=True, default=None, blank=True)
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

    @staticmethod
    def replace_flac_file_with_corrected_md5(file_path):
        result = subprocess.run(['flac', '-f', '--best', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stderr = result.stderr.decode()
        if 'ok' not in stderr:
            raise ValidationError("The Flac file md5 check failed and could not be corrected. The file is probably " +
                                  "corrupted.")

    def __str__(self) -> str:
        if self.file and self.file.name:
            return self.file.name + " (" + str(self.size_in_bytes) + " bytes)"
        return ""

    def save(self, *args, **kwargs):
        if self.file and self.file.name:
            self.filename = os.path.basename(self.file.name)
            self.extension = os.path.splitext(self.file.name)[1]
            self.size_in_bytes = self.file.size

        super().save(*args, **kwargs)  # So that the file is saved before the eventual md5 check

        if self.file and self.extension == '.flac':
            if not self.is_flac_file_md5_valid(self.file.path):
                self.replace_flac_file_with_corrected_md5(self.file.path)
                self.had_flac_md5_been_corrected = True
            else:
                self.had_flac_md5_been_corrected = False
            super().save(update_fields=[ATTRIBUTES_LABEL.HAD_FLAC_MD5_BEEN_CORRECTED])
