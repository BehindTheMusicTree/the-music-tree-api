
from bodzify_api.model.public_standard_resource.StandardResourceManager import \
    StandardResourceManager
from bodzify_api.model.trackable_play_count.Fields import \
    Fields as TrackablePlayCountFields
from bodzify_api.model.trackable_play_count.TrackablePlayCount import \
    TrackablePlayCount
from bodzify_api.serializer.model.play.input.schema.PostFields import \
    Fields as PostFields


class PlayManager(StandardResourceManager):

    def create(self, **kwargs):
        trackable_play_count_object: TrackablePlayCount = kwargs[PostFields.CONTENT]
        trackable_play_count_object.play_count += 1
        trackable_play_count_object.save(update_fields=[TrackablePlayCountFields.PLAY_COUNT])
        return super().create(**kwargs)
