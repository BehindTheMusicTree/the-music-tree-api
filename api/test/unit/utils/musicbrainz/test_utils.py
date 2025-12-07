import pytest

from api.model.musicbrainz_resource.children.recording.Fields import Fields as MusicbrainzRecordingFields
from api.utils.musicbrainz.utils import create_or_update_musicbrainz_recording_instance_from_dict
from api.z.ApiFields import ApiFields


@pytest.mark.django_db
class TestCreateOrUpdateMusicbrainzRecordingInstanceFromDict:
    def test_create_new_recording_then_created(self):
        musicbrainz_id = "4a45b00b-273d-40ed-9ecd-42f387f59c22"

        recording_dict = {
            ApiFields.Names.TITLE: "Drown (Massano remix)",
            ApiFields.Names.SCORE: 0.95,
            ApiFields.Names.DURATION_IN_SEC: 440,
            ApiFields.Names.ARTISTS: [
                {ApiFields.Names.ID: "artist-1", ApiFields.Names.NAME: "Artist 1"}
            ],
            ApiFields.Names.RELEASEGROUPS: []
        }

        recording = create_or_update_musicbrainz_recording_instance_from_dict(musicbrainz_id, recording_dict)

        assert recording.musicbrainz_id == musicbrainz_id
        assert recording.title == "Drown (Massano remix)"
        assert recording.score == 0.95
        assert recording.duration_in_sec == 440
        assert recording.musicbrainz_artists.count() == 1
        assert recording.musicbrainz_artists.first().musicbrainz_id == "artist-1"
        assert recording.musicbrainz_artists.first().name == "Artist 1"

    def test_update_existing_recording_then_updated(self):
        musicbrainz_id = "4a45b00b-273d-40ed-9ecd-42f387f59c22"

        recording_dict_1 = {
            ApiFields.Names.TITLE: "Old Title",
            ApiFields.Names.SCORE: 0.90,
            ApiFields.Names.DURATION_IN_SEC: 430,
            ApiFields.Names.ARTISTS: [
                {ApiFields.Names.ID: "artist-1", ApiFields.Names.NAME: "Artist 1"}
            ],
            ApiFields.Names.RELEASEGROUPS: []
        }

        recording_1 = create_or_update_musicbrainz_recording_instance_from_dict(musicbrainz_id, recording_dict_1)
        assert recording_1.title == "Old Title"
        assert recording_1.score == 0.90
        assert recording_1.duration_in_sec == 430

        recording_dict_2 = {
            ApiFields.Names.TITLE: "Drown (Massano remix)",
            ApiFields.Names.SCORE: 0.96,
            ApiFields.Names.DURATION_IN_SEC: 441,
            ApiFields.Names.ARTISTS: [
                {ApiFields.Names.ID: "artist-1", ApiFields.Names.NAME: "Artist 1"}
            ],
            ApiFields.Names.RELEASEGROUPS: []
        }

        recording_2 = create_or_update_musicbrainz_recording_instance_from_dict(musicbrainz_id, recording_dict_2)

        assert recording_2.musicbrainz_id == musicbrainz_id
        assert recording_2.id == recording_1.id
        assert recording_2.title == "Drown (Massano remix)"
        assert recording_2.score == 0.96
        assert recording_2.duration_in_sec == 441
