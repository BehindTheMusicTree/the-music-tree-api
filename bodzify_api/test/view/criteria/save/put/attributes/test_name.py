from rest_framework import status

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.schema.model.criteria.input.put import Fields as PutFields
from bodzify_api.test.field.body_data.method.PutBodyDataTestCase import PutBodyDataTestCase
from bodzify_api.test.field.body_data.type.not_nullable.PrimaryBodyDataTestCase import PrimaryBodyDataTestCase
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.utils import audio_metadata
from bodzify_api.utils.audio_metadata.NormalizedMetadataKeys import NormalizedMetadataKeys
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class TestCase(GenreTestCase, PutBodyDataTestCase, PrimaryBodyDataTestCase):

    def test_not_none_then_update(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_new_name = "Punk"
        response = self._put_genre(uuid=genre_rock.uuid, **{PutFields.NAME_PUBLIC: genre_new_name})
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_genre.name == genre_new_name

    def test_root_name_update(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        assert genre_rock.root.name == "Rock"

        genre_new_name = "Punk"
        response = self._put_genre(uuid=genre_rock.uuid, **{PutFields.NAME_PUBLIC: genre_new_name})
        assert response.status_code == status.HTTP_200_OK

        updated_genre = self.saved_genre
        assert updated_genre.name == genre_new_name
        assert updated_genre.root.name == genre_new_name

    def test_error_when_empty(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        response = self._put_genre(uuid=genre_rock.uuid, **{PutFields.NAME_PUBLIC: ""})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == PutFields.NAME_PUBLIC
        assert error['code'] == FieldValidationErrorCode.BLANK

    def test_not_provided_then_unchanged(self):
        genre_name = "Rock"
        genre = self.model_fixture_factory.create_genre(name=genre_name)

        response = self._put_genre(uuid=genre.uuid, **{PutFields.PARENT: None})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_genre.name == genre_name

    def test_ok_then_update_linked_lib_track(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        track = self.model_fixture_factory.create_lib_track_with_file(title="Track", genre=genre_rock)

        genre_new_name = "Punk"
        response = self._put_genre(uuid=genre_rock.uuid, **{PutFields.NAME_PUBLIC: genre_new_name})

        assert response.status_code == status.HTTP_200_OK
        updated_track: LibraryTrack = LibraryTrack.objects.get(uuid=track.uuid)
        metadata = audio_metadata.get_normalized_metadata_from_file(file=updated_track.track_file.file)
        assert metadata[NormalizedMetadataKeys.GENRE_NAME] == genre_new_name
