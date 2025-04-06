from rest_framework import status

from bodzify_api.serializer.model.uploaded_track.input.put.Fields import Fields as PutFields
from bodzify_api.test.utils.field.body_data.method.PutBodyDataTestCase import PutBodyDataTestCase
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase, PutBodyDataTestCase):

    def test_not_empty_then_ok(self):
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(title="Love")

        title_new = "a"
        response = self._put_uploaded_track(uploaded_track.uuid, **{PutFields.TITLE: title_new})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.title == title_new

    def test_not_provided_then_unchanged(self):
        old_title = "Love"
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(title=old_title)

        response = self._put_uploaded_track(uploaded_track.uuid, **{PutFields.ARCHIVED: True})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.title == old_title

    def test_empty_then_400_bad_request(self):
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(title="Love")

        response = self._put_uploaded_track(uploaded_track.uuid, **{PutFields.TITLE: ""}
                                            )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_provided_then_update(self):
        title = "a"
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(title=title)

        response = self._put_uploaded_track(uploaded_track.uuid, **{PutFields.TITLE: title})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.title == title
