from rest_framework import status

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.schema.model.criteria.input.put import Fields as PutFields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase
from bodzify_api.utils import audio_metadata
from bodzify_api.utils.audio_metadata.NormalizedMetadataKeys import NormalizedMetadataKeys


class TestCase(GenreTestCase):

    def test_ok(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        genre_new_name = "Punk"
        response = self._put_genre(uuid=rock_genre.uuid, **{PutFields.NAME: genre_new_name})
        assert response.status_code == status.HTTP_200_OK
        print('self.saved_genre')
        print(self.saved_genre)
        assert self.saved_genre.name == genre_new_name

    def test_root_name_update(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        assert rock_genre.root.name == "Rock"

        genre_new_name = "Punk"
        response = self._put_genre(uuid=rock_genre.uuid, **{PutFields.NAME: genre_new_name})
        assert response.status_code == status.HTTP_200_OK

        updated_genre = self.saved_genre
        assert updated_genre.name == genre_new_name
        assert updated_genre.root.name == genre_new_name

    def test_error_when_empty(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        response = self._put_genre(uuid=rock_genre.uuid, **{PutFields.NAME: ""})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_provided_then_unchanged(self):
        genre_name = "Rock"
        genre = self.model_fixture_factory.create_genre(name=genre_name)
        response = self._put_genre(uuid=genre.uuid)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_genre.name == genre_name

    def test_ok_then_update_linked_lib_track(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")

        track = self.model_fixture_factory.create_lib_track_with_file(
            title='polo',
            genre_name=rock_genre.name,
            user=self.test_user1
        )

        genre_new_name = "Punk"
        response = self._put_genre(uuid=rock_genre.uuid, **{PutFields.NAME: genre_new_name})
        assert response.status_code == status.HTTP_200_OK

        updated_track: LibraryTrack = LibraryTrack.objects.get(uuid=track.uuid)
        metadata = audio_metadata.get_normalized_metadata_from_file(file=updated_track.track_file.file)
        assert metadata[NormalizedMetadataKeys.GENRE_NAME] == gen
