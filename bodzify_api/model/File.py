import os

from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

from bodzify_api.validator.track_file_validator \
    import validate_size, validate_is_audio, validate_content_type_is_audio, validate_filename_length
from bodzify_api import settings


class ATTRIBUTES_LABEL:
    FILE = 'file'
    FILENAME = 'filename'
    EXTENSION = 'extension'
    SIZE_IN_BYTES = 'size_in_bytes'
    SIZE_IN_KO = 'size_in_ko'
    SIZE_IN_MO = 'size_in_mo'


def _get_user_directory_path(instance, filename):
    return '{0}{1}/{2}'.format(settings.LIB_DIR_NAME + '/' + settings.USER_LIB_DIR_NAME_PREFIXE,
                               instance.user.id,
                               filename)


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    file = models.FileField(upload_to=_get_user_directory_path,
                            help_text="Only audio formats accepted.",
                            validators=[FileExtensionValidator(settings.LIB_TRACK_FILE_EXTENSIONS),
                                        validate_filename_length,
                                        validate_size,
                                        validate_content_type_is_audio],
                            null=True)
    filename = models.CharField(max_length=255, blank=True)
    extension = models.CharField(max_length=5, blank=True)
    size_in_bytes = models.FloatField(null=True, blank=True)
    size_in_ko = models.GeneratedField(
        expression=F(ATTRIBUTES_LABEL.SIZE_IN_BYTES) / 1024,
        output_field=models.FloatField(),
        db_persist=True,
    )
    size_in_mo = models.GeneratedField(
        expression=F(ATTRIBUTES_LABEL.SIZE_IN_BYTES) / (1024 * 1024),
        output_field=models.FloatField(),
        db_persist=True,
    )

    def __str__(self) -> str:
        if self.file and self.file.name:
            return self.file.name + " (" + str(self.size_in_bytes) + " bytes)"
        return ""

    def save(self, *args, **kwargs):
        if self.file and self.file.name:
            self.filename = os.path.basename(self.file.name)
            self.extension = os.path.splitext(self.file.name)[1]
            self.size_in_bytes = self.file.size
        super().save(*args, **kwargs)
