from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from api.model.uploaded_track.file.TrackFile import TrackFile
    from api.model.user.User import User


def get_user_lib_path(instance: 'TrackFile', filename):
    user: User = instance.user
    return user.lib_path_relative_to_media + '/' + filename
