
from rest_framework import status


from bodzify_api.serializer.schema.artist.detailed import Fields as ArtistFields
from bodzify_api.test.view.artist.ArtistTestCase import ArtistTestCase
from bodzify_api.utils.utils import to_camel_case
from bodzify_api.serializer.schema.lib_track.input.endpoint.post import Fields as LibTrackPostFields


class TestCase(ArtistTestCase):

    def test_duration(self):
        artist = self.model_fixture_factory.create_artist(name="Sum 41")
        self.model_fixture_factory.create_lib_track_with_file(title='celine',
                                                              filename="Celinekin Park 284 sec.mp3",
                                                              artists=[artist])
        self.model_fixture_factory.create_lib_track_with_file(title='tokyo',
                                                              filename="tokyo drift x sean paul 152 sec.mp3",
                                                              artists=[artist])
        response = self._retrieve(artist.uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[to_camel_case(ArtistFields.DURATION_IN_SEC)] == 284 + 152

    def test_count(self):
        artist = self.model_fixture_factory.create_artist(name="Sum 41")
        self.model_fixture_factory.create_lib_track_with_file(title="In Too Deep", artists=[artist])
        self.model_fixture_factory.create_lib_track_with_file(title="Summer", artists=[artist])
        response = self._retrieve(artist.uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[to_camel_case(ArtistFields.LIB_TRACKS_COUNT)] == 2

    def test_archived_count(self):
        artist = self.model_fixture_factory.create_artist(name="Sum 41")
        self.model_fixture_factory.create_lib_track_with_file(title="In Too Deep", artists=[artist])
        self.model_fixture_factory.create_lib_track_with_file(title="Summer", artists=[artist], archived=True)
        self.model_fixture_factory.create_lib_track_with_file(title="Summer2", artists=[artist], archived=True)
        self.model_fixture_factory.create_lib_track_with_file(title="Summer3", artists=[artist], archived=True)
        response = self._retrieve(artist.uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[to_camel_case(ArtistFields.LIB_TRACKS_ARCHIVED_COUNT)] == 3
