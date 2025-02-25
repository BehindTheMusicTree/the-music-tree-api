from rest_framework import status

from bodzify_api.serializer.model.lib_track.output.Fields import \
    Fields as LibTrackFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.utils import data_transformer


class TestCase(LibTrackTestCase):

    def test_language_and_genre_name_then_ok(self):
        genre = self.model_fixture_factory.create_genre(name="Rock")
        track = self.model_fixture_factory.create_lib_track_with_file(
            title="Life", language="en", genre=genre)
        self.model_fixture_factory.create_lib_track_with_file(title="Hey", language="fr")
        self.model_fixture_factory.create_lib_track_with_file(title="Rockaille", language="en")

        response = self._get_lib_tracks(language='en', genre_name='Roc')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        assert self.results[0][data_transformer.to_camel_case(LibTrackFields.TITLE)] == track.title

    def test_title_and_album_name_and_artists_name_ok(self):
        genre = self.model_fixture_factory.create_genre(name="Heyaa")
        album_best = self.model_fixture_factory.create_album(name="Best ok")
        album_besto = self.model_fixture_factory.create_album(name="Besto")
        artist_john = self.model_fixture_factory.create_artist(name="John")
        artist_jony = self.model_fixture_factory.create_artist(name="Jony")

        self.model_fixture_factory.create_lib_track_with_file(
            title="Life", language="en", genre=genre)
        track_pascalito = self.model_fixture_factory.create_lib_track_with_file(title="Pascalito",
                                                                                album=album_best,
                                                                                artists=[artist_john])
        track_mapasa = self.model_fixture_factory.create_lib_track_with_file(title="mapasa",
                                                                             album=album_besto,
                                                                             artists=[artist_john, artist_jony])
        self.model_fixture_factory.create_lib_track_with_file(title="Hey", album=album_best, artists=[artist_john])
        self.model_fixture_factory.create_lib_track_with_file(title="sd", album=album_besto, artists=[artist_jony])
        self.model_fixture_factory.create_lib_track_with_file(title="Hey",
                                                              album=album_best,
                                                              artists=[artist_john, artist_jony])

        response = self._get_lib_tracks(title='pas', album_name='Best', artists_name='Joh')

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        titles = self.results[0][
            data_transformer.to_camel_case(LibTrackFields.TITLE)], self.results[1][
            data_transformer.to_camel_case(LibTrackFields.TITLE)]
        assert track_pascalito.title in titles
        assert track_mapasa.title in titles
