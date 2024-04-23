from django.db import models
from django.db.models import F
import os


class ATTRIBUTES_LABEL:
    FILE = 'file'
    FILENAME = 'filename'
    EXTENSION = 'extension'
    SIZE_IN_BYTES = 'size_in_bytes'
    SIZE_IN_KB = 'size_in_kb'
    SIZE_IN_MO = 'size_in_mo'


class File(models.Model):
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
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
