from django.core.exceptions import ValidationError
from bodzify_api.model.base.BaseManager import BaseManager
from bodzify_api.model.playlist.children.Fields import Fields as ModelFields


class ChildPlaylistManager(BaseManager):

    def _update_base_playlist_kwargs(self, kwargs):
        fields_to_update = [
            ModelFields.UUID,
            ModelFields.USER,
            ModelFields.CREATED_ON,
            ModelFields.UPDATED_ON
        ]

        for field in fields_to_update:
            if field in kwargs:
                kwargs[f'{ModelFields.BASE_PLAYLIST}__{field}'] = kwargs.pop(field)

    def filter(self, *args, **kwargs):
        self._update_base_playlist_kwargs(kwargs)
        return super().filter(*args, **kwargs)

    def get(self, *args, **kwargs):
        self._update_base_playlist_kwargs(kwargs)
        return super().get(*args, **kwargs)

    def get_or_create(self, **kwargs):
        self._update_base_playlist_kwargs(kwargs)
        return super().get_or_create(**kwargs)

    def create(self, user, *args, **kwargs):
        from bodzify_api.model.playlist.BasePlaylist import BasePlaylist

        model_class = self.model
        if model_class._meta.abstract:
            raise ValueError(f"Cannot create an instance of abstract class {model_class.__name__}")

        if not user:
            raise ValueError("User must be provided when creating a ChildPlaylist")

        base_playlist = kwargs.pop(ModelFields.BASE_PLAYLIST, None)
        if base_playlist:
            raise ValidationError("base_playlist must not be provided when creating a ChildPlaylist")

        kwargs[ModelFields.BASE_PLAYLIST] = base_playlist

        instance = super().create(*args, **kwargs)

        base_playlist = BasePlaylist.objects.create(
            user=user, object_pk=instance.pk, content_type=instance.content_type)

        return instance

    def order_by(self, *args):
        updated_args = []
        for arg in args:
            if arg.lstrip('-') in [
                ModelFields.UUID,
                ModelFields.USER,
                ModelFields.CREATED_ON,
                ModelFields.UPDATED_ON
            ]:
                updated_args.append(f'{ModelFields.BASE_PLAYLIST}__{arg}')
            else:
                updated_args.append(arg)
        return super().order_by(*updated_args)
