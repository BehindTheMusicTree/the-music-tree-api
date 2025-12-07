from rest_framework import status

from api.model.uploaded_track_playlist_rel.UploadedTrackPlaylistRel import UploadedTrackPlaylistRel
from api.serializer.model.criteria.input.put import Fields as PutFields
from api.test.integration.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_new_parent_then_tracks_in_same_order_and_added_at_the_beginning(self) -> None:
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        uploaded_track_rock_added_first = self.model_fixture_factory.create_uploaded_track_with_file(
            title="kok", genre=genre_rock, use_manager_for_genre_playlist_adding=True)
        uploaded_track_rock_added_second = self.model_fixture_factory.create_uploaded_track_with_file(
            title="lkdw", genre=genre_rock, use_manager_for_genre_playlist_adding=True)

        genre_punk = self.model_fixture_factory.create_genre(name="Punk")
        uploaded_track_punk_added_third = self.model_fixture_factory.create_uploaded_track_with_file(
            title="punk song", genre=genre_punk, use_manager_for_genre_playlist_adding=True)
        uploaded_track_punk_added_fourth = self.model_fixture_factory.create_uploaded_track_with_file(
            title="loul", genre=genre_punk, use_manager_for_genre_playlist_adding=True)

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: genre_rock.uuid})

        assert response.status_code == status.HTTP_200_OK

        rock_playlist_uploaded_tracks_not_archived_dict_by_position = \
            genre_rock.criteria_playlist.uploaded_tracks_not_archived_dict_by_position
        assert rock_playlist_uploaded_tracks_not_archived_dict_by_position[1] == uploaded_track_punk_added_fourth
        assert rock_playlist_uploaded_tracks_not_archived_dict_by_position[2] == uploaded_track_punk_added_third
        assert rock_playlist_uploaded_tracks_not_archived_dict_by_position[3] == uploaded_track_rock_added_second
        assert rock_playlist_uploaded_tracks_not_archived_dict_by_position[4] == uploaded_track_rock_added_first

    def test_new_parent_then_tracks_in_same_order_and_added_at_the_beginning_of_parent_of_parent(self) -> None:
        genre_guitare = self.model_fixture_factory.create_genre(name="Guitare")
        uploaded_track_previously_second_in_guitare = self.model_fixture_factory.create_uploaded_track_with_file(
            title="guitare2", genre=genre_guitare, use_manager_for_genre_playlist_adding=True)
        uploaded_track_previously_first_in_guitare = self.model_fixture_factory.create_uploaded_track_with_file(
            title="guitare1", genre=genre_guitare, use_manager_for_genre_playlist_adding=True)

        assert genre_guitare.criteria_playlist.uploaded_tracks.count() == 2
        assert genre_guitare.criteria_playlist.uploaded_track_playlist_rels.get(
            uploaded_track=uploaded_track_previously_first_in_guitare).position == 1
        assert genre_guitare.criteria_playlist.uploaded_track_playlist_rels.get(
            uploaded_track=uploaded_track_previously_second_in_guitare).position == 2

        genre_rock = self.model_fixture_factory.create_genre(name="Rock", parent=genre_guitare)

        uploaded_track_previously_second_in_rock = self.model_fixture_factory.create_uploaded_track_with_file(
            title="rock2",
            genre=genre_rock,
            use_manager_for_genre_playlist_adding=True)
        uploaded_track_previously_first_in_rock = self.model_fixture_factory.create_uploaded_track_with_file(
            title="rock1",
            genre=genre_rock,
            use_manager_for_genre_playlist_adding=True)

        genre_punk = self.model_fixture_factory.create_genre(name="Punk")
        uploaded_track_previously_second_in_punk = self.model_fixture_factory.create_uploaded_track_with_file(
            title="punk2",
            genre=genre_punk,
            use_manager_for_genre_playlist_adding=True)
        uploaded_track_previously_first_in_punk = self.model_fixture_factory.create_uploaded_track_with_file(
            title="punk1",
            genre=genre_punk,
            use_manager_for_genre_playlist_adding=True)

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: genre_rock.uuid})
        assert response.status_code == status.HTTP_200_OK
        uploaded_track_playlist_rels: list[UploadedTrackPlaylistRel] = list(
            UploadedTrackPlaylistRel.objects.filter(
                user=self.test_user1, playlist=genre_guitare.criteria_playlist))
        tracks_uuids_positions = {
            relation.uploaded_track.uuid: relation.position for relation in uploaded_track_playlist_rels}
        assert tracks_uuids_positions[uploaded_track_previously_first_in_punk.uuid] == 1
        assert tracks_uuids_positions[uploaded_track_previously_second_in_punk.uuid] == 2
        assert tracks_uuids_positions[uploaded_track_previously_first_in_rock.uuid] == 3
        assert tracks_uuids_positions[uploaded_track_previously_second_in_rock.uuid] == 4
        assert tracks_uuids_positions[uploaded_track_previously_first_in_guitare.uuid] == 5
        assert tracks_uuids_positions[uploaded_track_previously_second_in_guitare.uuid] == 6

    def test_new_parent_not_acendant_of_old_parent_then_update_positions_in_old_parent(self) -> None:
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        track_rock_added_first = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Rock song 2", genre=genre_rock, use_manager_for_genre_playlist_adding=True)
        track_punk_added_second = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Punk song 2", genre=genre_punk, use_manager_for_genre_playlist_adding=True)
        track_rock_added_third = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Rock song 1", genre=genre_rock, use_manager_for_genre_playlist_adding=True)
        track_punk_added_forth = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Punk song 1", genre=genre_punk, use_manager_for_genre_playlist_adding=True)

        rock_playlist_uploaded_tracks_not_archived_dict_by_position = \
            genre_rock.criteria_playlist.uploaded_tracks_not_archived_dict_by_position
        assert rock_playlist_uploaded_tracks_not_archived_dict_by_position[1] == track_punk_added_forth
        assert rock_playlist_uploaded_tracks_not_archived_dict_by_position[2] == track_rock_added_third
        assert rock_playlist_uploaded_tracks_not_archived_dict_by_position[3] == track_punk_added_second
        assert rock_playlist_uploaded_tracks_not_archived_dict_by_position[4] == track_rock_added_first

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: ''})

        assert response.status_code == status.HTTP_200_OK
        rock_playlist_uploaded_tracks_not_archived_dict_by_position = \
            genre_rock.criteria_playlist.uploaded_tracks_not_archived_dict_by_position
        assert len(rock_playlist_uploaded_tracks_not_archived_dict_by_position) == 2
        assert rock_playlist_uploaded_tracks_not_archived_dict_by_position[1] == track_rock_added_third
        assert rock_playlist_uploaded_tracks_not_archived_dict_by_position[2] == track_rock_added_first

    def test_new_parent_undirect_ascendant_of_old_parent_then_update_positions_in_criterias_in_between(self) -> None:
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        punk_fr_genre = self.model_fixture_factory.create_genre(name="Punk FR", parent=genre_punk)

        track_second_in_punk = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Punk song", genre=genre_punk, use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="punk fr song", genre=punk_fr_genre, use_manager_for_genre_playlist_adding=True)

        response = self._put_genre(uuid=punk_fr_genre.uuid, **{PutFields.PARENT: genre_rock.uuid})

        assert response.status_code == status.HTTP_200_OK
        uploaded_track_playlist_rel: UploadedTrackPlaylistRel = \
            UploadedTrackPlaylistRel.objects.get(user=self.test_user1,
                                                 playlist=genre_punk.criteria_playlist,
                                                 uploaded_track=track_second_in_punk)
        assert uploaded_track_playlist_rel.position == 1
