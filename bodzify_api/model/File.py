from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
import os
from django.core.validators import FileExtensionValidator
from bodzify_api.validator.TrackFileValidator import validate_size


from bodzify_api import settings


class ATTRIBUTES_LABEL:
    FILE = 'file'
    FILENAME = 'filename'
    EXTENSION = 'extension'
    SIZE_IN_BYTES = 'size_in_bytes'
    SIZE_IN_KB = 'size_in_kb'
    SIZE_IN_MO = 'size_in_mo'


def _get_user_directory_path(instance, filename):
    return '{0}{1}/{2}'.format(settings.LIB_DIR_NAME + '/' + settings.USER_LIB_DIR_NAME_PREFIXE,
                               instance.user.id,
                               filename)


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    file = models.FileField(upload_to=_get_user_directory_path,
                            help_text="Only audio formats accepted.",
                            validators=[FileExtensionValidator(settings.LIB_TRACK_FILE_EXTENSIONS), validate_size],
                            null=True)
    filename = models.CharField(max_length=255, blank=True)
    extension = models.CharField(max_length=5, blank=True)
    size_in_bytes = models.IntegerField(blank=True, null=True)
    size_in_kb = models.FloatField(blank=True, null=True)
    size_in_mo = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.filename = os.path.basename(self.file.name)
        self.extension = os.path.splitext(self.file.name)[1]
        self.size_in_bytes = self.file.size
        self.size_in_kb = self.file.size / 1024
        self.size_in_mo = self.file.size / (1024 * 1024)
        super().save(*args, **kwargs)
