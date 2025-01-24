from unittest.mock import patch

from bodzify_api.model.user.User import User
from bodzify_api.test.view.user.UserTestCase import UserTestCase


class TestCase(UserTestCase):

    def test_exception_then_rollback(self):
        user = self.model_fixture_factory.create_user('jojo')
        self.model_fixture_factory.create_lib_track_with_file(user=user, title="joie")
        with patch('bodzify_api.model.track.lib.LibraryTrack.LibraryTrack.save') as mock:
            exception_message = "Save failed!"
            mock.side_effect = Exception(exception_message)

            try:
                self._delete_user(user.pk)
            except Exception as e:
                assert str(e) == exception_message
                assert User.objects.filter(pk=user.pk).exists()
