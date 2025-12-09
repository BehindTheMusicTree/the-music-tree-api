from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from api.model.track.Track import Track
    from api.model.user.User import User


def get_user_lib_path(instance: 'Track', filename):
    user: User = instance.user
    return user.lib_path_relative_to_media + '/' + filename
