import os
from pathlib import Path
import shutil
from typing import TYPE_CHECKING

from django.contrib.auth.models import AbstractUser
from django.utils.functional import cached_property
from django.db import models
from django.db.models import F, Value

from bodzify_api import settings
from bodzify_api.model.base.BaseModel import BaseModel
from bodzify_api.model.utils.ConcatOp import ConcatOp
from bodzify_api.model.utils.ConditionalExpression import ConditionalExpression
from .UserManager import UserManager
from .Fields import Fields

if TYPE_CHECKING:
    from bodzify_api.model.all_lib_tracks_mixin.AllLibTracksMixin import AllLibTracksMixin


class User(AbstractUser, BaseModel):
    DEFAULT_LIB_TRACK_FILENAME_WITH_EXTENSION = "default.mp3"

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
            output_field=models.CharField(max_length=255)),
        output_field=models.CharField(max_length=255),
        db_persist=True)

    objects: UserManager = UserManager()

    @property
    def lib_abs_path(self) -> Path:
        return settings.MEDIA_ROOT / self.lib_path_relative_to_media

    @cached_property
    def all_lib_tracks_mixin(self) -> 'AllLibTracksMixin':
        from bodzify_api.model.all_lib_tracks_mixin.AllLibTracksMixin import AllLibTracksMixin
        all_lib_tracks_mixin, _ = AllLibTracksMixin.objects.get_or_create(user=self)
        return all_lib_tracks_mixin

    @property
    def default_lib_track_file_abs_path(self):
        return self.lib_abs_path / self.DEFAULT_LIB_TRACK_FILENAME_WITH_EXTENSION

    def _empty_user_library(self):
        for filename in os.listdir(self.lib_abs_path):
            filePath = os.path.join(self.lib_abs_path, filename)
            try:
                if os.path.isfile(filePath) or os.path.islink(filePath):
                    os.unlink(filePath)
                elif os.path.isdir(filePath):
                    shutil.rmtree(filePath)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (filePath, e))

    def copy_file_to_lib(self, file_abs_path: Path):
        shutil.copy(file_abs_path, self.lib_abs_path)

    def does_track_filename_exist_in_lib(self, filename: str):
        return os.path.isfile(Path(self.lib_abs_path) / filename)

    def delete(self, *args, **kwargs):
        if self.lib_abs_path.exists():
            shutil.rmtree(self.lib_abs_path)

        super().delete(*args, **kwargs)
