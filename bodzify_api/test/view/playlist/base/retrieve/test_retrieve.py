#!/usr/bin/env python

from rest_framework import status

from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.serializer.playlist.base.output.with_tracks import FIELDS as RETRIEVE_FIELDS
from bodzify_api.test.view.playlist.base.BasePlaylistTestCase import BasePlaylistTestCase
from bodzify_api.utils import to_camel_case
from bodzify_api.serializer.track.output.without_playlists_and_album import FIELDS as LIB_TRACK_FIELDS
from bodzify_api.serializer.playlist_lib_track_relation.output.without_playlist \
    import FIELDS as playlist_lib_track_relation_RELATION_FIELDS


class TestCase(BasePlaylistTestCase):

    def test_retrieve_simple_then_ok(self):
        name = 'cuisine'
        playlist_uuid = self.model_fixture_factory.create_simple_playlist(name=name).base_playlist.uuid

        response = self.retrieve_playlist(uuid=playlist_uuid)
        assert response.status_code == status.HTTP_200_OK
        assert self.result[RETRIEVE_FIELDS.NAME] == name

    def test_retrieve_genre_then_ok(self):
        name = 'rock'
        genre = self.model_fixture_factory.create_genre(name=name)
        playlist_uuid = BasePlaylist.objects.get(
            criteria_playlist__criteria=genre,
            criteria_playlist__type=CRITERIA_TYPES_ID.GENRE).uuid

        response = self.retrieve_playlist(uuid=playlist_uuid)
        assert response.status_code == status.HTTP_200_OK
        assert self.result[RETRIEVE_FIELDS.NAME] == name

    def test_retrieve_tag_then_ok(self):
        name = 'fr'
        genre = self.model_fixture_factory.create_tag(name=name)
        playlist_uuid = BasePlaylist.objects.get(
            criteria_playlist__criteria=genre,
            criteria_playlist__type=CRITERIA_TYPES_ID.TAG).uuid

        response = self.retrieve_playlist(uuid=playlist_uuid)
        assert response.status_code == status.HTTP_200_OK
        assert self.result[RETRIEVE_FIELDS.NAME] == name

    def test_retrieve_then_lib_track_ordered_by_position(self):
        genre_name = 'rock'
        genre = self.model_fixture_factory.create_tag(name=genre_name)

        lib_track3 = self.model_fixture_factory.create_lib_track(title="Love", genre=genre)
        lib_track2 = self.model_fixture_factory.create_lib_track(title="Loves", genre=genre)
        lib_track1 = self.model_fixture_factory.create_lib_track(title="Lovdddde", genre=genre)

        response = self.retrieve_playlist(uuid=genre.criteria_playlist.base_playlist.uuid)  # type: ignore
        assert response.status_code == status.HTTP_200_OK
        result_tracks = self.result[to_camel_case(RETRIEVE_FIELDS.LIB_TRACKS)]
        assert result_tracks[0][to_camel_case(playlist_lib_track_relation_RELATION_FIELDS.LIB_TRACK)][
            LIB_TRACK_FIELDS.TITLE] == lib_track1.title
        assert result_tracks[1][to_camel_case(playlist_lib_track_relation_RELATION_FIELDS.LIB_TRACK)][
            LIB_TRACK_FIELDS.TITLE] == lib_track2.title
        assert result_tracks[2][to_camel_case(playlist_lib_track_relation_RELATION_FIELDS.LIB_TRACK)][
            LIB_TRACK_FIELDS.TITLE] == lib_track3.title
