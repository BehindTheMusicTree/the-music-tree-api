import os
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Value
from django.utils.functional import cached_property

from api import settings
from api.model.base.BaseModel import BaseModel
from api.model.field.AppCharField import AppCharField
from api.model.utils.ConcatOp import ConcatOp
from api.model.utils.ConditionalExpression import ConditionalExpression
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename

from .Fields import Fields
from .UserManager import UserManager


if TYPE_CHECKING:
    from api.model.all_uploaded_tracks_mixin.AllUploadedTracksMixin import AllUploadedTracksMixin


class User(AbstractUser, BaseModel):
    DEFAULT_UPLOADED_TRACK_FILENAME_WITH_EXTENSION = "default.mp3"

    is_test_user = models.BooleanField(default=False)
    lib_path_relative_to_media = models.GeneratedField(  # type: ignore
        expression=ConditionalExpression(
            condition_field=Fields.IS_TEST_USER,
            when_true=ConcatOp(Value(str(settings.LIBRARIES_DIR_NAME)),
                               Value('/'),
                               Value(settings.TEST_USER_LIBRARIES_DIR_NAME_PREFIXE),
                               F(Fields.ID)),
            when_false=ConcatOp(Value(str(settings.LIBRARIES_DIR_NAME)),
                                Value('/'),
                                Value(settings.USER_LIBRARIES_DIR_NAME_PREFIXE),
                                F(Fields.ID)),
            output_field=AppCharField(max_length=256)),
        output_field=AppCharField(max_length=256),
        db_persist=True)

    objects: UserManager = UserManager()

    @property
    def lib_abs_path(self) -> Path:
        return settings.MEDIA_ROOT / self.lib_path_relative_to_media

    @cached_property
    def all_uploaded_tracks_mixin(self) -> 'AllUploadedTracksMixin':
        from api.model.all_uploaded_tracks_mixin.AllUploadedTracksMixin import AllUploadedTracksMixin
        all_uploaded_tracks_mixin, _ = AllUploadedTracksMixin.objects.get_or_create(user=self)
        return all_uploaded_tracks_mixin

    def does_track_filename_exist_in_lib(self, test_uploaded_track_filename: UploadedTrackTestFilename):
        return os.path.isfile(Path(self.lib_abs_path) / test_uploaded_track_filename.value)

    def delete(self, *args, **kwargs):
        if self.lib_abs_path.exists():
            shutil.rmtree(self.lib_abs_path)

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
