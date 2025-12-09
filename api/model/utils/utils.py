from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from api.model.uploaded_track.UploadedTrack import UploadedTrack
    from api.model.user.User import User


def get_user_lib_path(instance: 'UploadedTrack', filename):
    user: User = instance.user
    return user.lib_path_relative_to_media + '/' + filename
