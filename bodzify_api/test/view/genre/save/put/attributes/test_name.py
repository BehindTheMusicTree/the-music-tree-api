from rest_framework import status

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.schema.model.criteria.input.endpoint.put import Fields as PutFields
from bodzify_api.serializer.schema.model.lib_track.input.endpoint.post import Fields as LibTrackPostFields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase
from bodzify_api.utils import audio_metadata
from bodzify_api.utils.audio_metadata.NormalizedMetadataKeys import NormalizedMetadataKeys


class TestCase(GenreTestCase):

    def test_ok(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        genre_new_name = "Punk"
        response = self._put_genre(uuid=rock_genre.uuid, **{PutFields.NAME: genre_new_name})
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_genre.name == genre_new_name

    def test_error_when_name_is_empty(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        response = self._put_genre(uuid=rock_genre.uuid, **{PutFields.NAME: ""})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.saved_genre.name == "Rock"

    def test_not_provided_then_unchanged(self):
        genre_name = "Rock"
        genre = self.model_fixture_factory.create_genre(name=genre_name)
        response = self._put_genre(uuid=genre.uuid, **{})
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_genre.name == genre_name

    def test_ok_then_update_linked_lib_track(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")

        data = {LibTrackPostFields.GENRE_NAME: rock_genre.name}
        track = self.model_fixture_factory.create_lib_track_with_file(title='polo', **data)

        genre_new_name = "Punk"
        response = self._put_genre(uuid=rock_genre.uuid, **{PutFields.NAME: genre_new_name})
        assert response.status_code == status.HTTP_200_OK

        updated_track: LibraryTrack = LibraryTrack.objects.get(uuid=track.uuid)
        metadata = audio_metadata.get_normalized_metadata_from_file(file=updated_track.track_file.file)
        assert metadata[NormalizedMetadataKeys.GENRE_NAME] == genre_new_name
