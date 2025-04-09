from typing import TYPE_CHECKING, TypeVar

from django.contrib.auth.models import BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from bodzify_api import settings
from bodzify_api.model.base.BaseManager import BaseManager
from bodzify_api.model.criteria.type.CriteriaType import CriteriaType
from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist

from .Fields import Fields


if TYPE_CHECKING:
    from bodzify_api.model.user.User import User


T = TypeVar('T', bound='User')


class UserManager(BaseManager[T], BaseUserManager):
    def get_default_ordering(self):
        return [Fields.USERNAME]

    def create_instance(self, **kwargs) -> T:
        if not kwargs[Fields.EMAIL]:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(kwargs.pop(Fields.EMAIL))
        password = kwargs.pop(Fields.PASSWORD)

        user: T = self.model(username=kwargs.pop(Fields.USERNAME), email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields) -> T:
        extra_fields.setdefault(Fields.IS_STAFF, True)
        extra_fields.setdefault(Fields.IS_SUPERUSER, True)

        if extra_fields.get(Fields.IS_STAFF) is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get(Fields.IS_SUPERUSER) is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_instance(username=username, email=email, password=password, **extra_fields)

    def delete_instance(self, instance: T):
        with transaction.atomic():
            instance.delete()


@receiver(post_save, sender=settings.APP_NAME + '.User')
def create_user_criterialess_playlists(sender, instance, created, **kwargs):
    if created:
        for criteria_type in [CriteriaTypePks.GENRE, CriteriaTypePks.TAG]:
            type = CriteriaType.objects.get(pk=criteria_type)
            CriteriaPlaylist.objects.create(user=instance, type=type, criteria=None)

        from bodzify_api.model.all_uploaded_tracks_mixin.AllUploadedTracksMixin import AllUploadedTracksMixin
        AllUploadedTracksMixin.objects.create(user=instance)
