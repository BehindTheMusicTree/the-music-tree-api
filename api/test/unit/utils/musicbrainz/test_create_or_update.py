import pytest

from api.utils.musicbrainz.utils import create_or_update_musicbrainz_recording_instance_from_dict
from api.z.ApiFields import ApiFields


@pytest.mark.django_db
class TestCreateOrUpdateMusicbrainzRecordingInstanceFromDict:
    def test_upload_same_track_twice_then_title_updated(self):
        musicbrainz_id = "4a45b00b-273d-40ed-9ecd-42f387f59c22"

        recording_dict_1 = {
            ApiFields.Names.TITLE: "Drown (Massano remix)",
            ApiFields.Names.SCORE: 0.95,
            ApiFields.Names.DURATION_IN_SEC: 440,
            ApiFields.Names.ARTISTS: [
                {ApiFields.Names.ID: "artist-1", ApiFields.Names.NAME: "Artist 1"}
            ],
            ApiFields.Names.RELEASEGROUPS: []
        }

        recording_1 = create_or_update_musicbrainz_recording_instance_from_dict(musicbrainz_id, recording_dict_1)
        assert recording_1.musicbrainz_id == musicbrainz_id
        assert recording_1.title == "Drown (Massano remix)"
        assert recording_1.score == 0.95
        assert recording_1.duration_in_sec == 440

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
