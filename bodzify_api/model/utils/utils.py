from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from bodzify_api.model.user.User import User
    from bodzify_api.model.track.file.TrackFile import TrackFile


def get_user_lib_path(instance: 'TrackFile', filename):
    user: User = instance.user
    return user.lib_path_relative_to_media + '/' + filename
