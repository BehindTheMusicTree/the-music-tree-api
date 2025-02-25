from django.db import models

from bodzify_api.model.private_unique_resource.PrivateUniqueResource import \
    PrivateUniqueResource


class TrackablePlayCount(PrivateUniqueResource):
    play_count = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
