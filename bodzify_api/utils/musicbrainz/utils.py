
import datetime
from calendar import monthrange
from uuid import UUID

from bodzify_api.model.musicbrainz.MusicbrainzArtist import Fields as MusicbrainzArtistFields, MusicbrainzArtist
from bodzify_api.model.musicbrainz.recording.MusicbrainzRecording import \
    MusicbrainzRecording, Fields as MusicbrainzRecordingFields


class ApiFields:
    class Names:
        RESULTS = 'results'
        RECORDINGS = 'recordings'
        ID = 'id'
        SCORE = 'score'
        ARTISTS = 'artists'
        NAME = 'name'
        TITLE = 'title'
        DATE = 'date'
        DURATION_IN_SEC = 'duration'
        RELEASEGROUPS = 'releasegroups'
        RELEASES = 'releases'
        DAY = 'day'
        MONTH = 'month'
        YEAR = 'year'
        ERROR = 'error'
        STATUS = 'status'
        CODE = 'code'
        MESSAGE = 'message'

    class Values:
        class Status:
            OK = 'ok'
            ERROR = 'error'


def get_best_recording_dict_with_score(recordings_grouped_by_score, duration_in_sec):
    def rate_groupe_of_recordings_by_score(group_of_recordings):
        return group_of_recordings[ApiFields.Names.SCORE]

    def rate_recording_by_similar_duration_and_by_number_of_fields(recording):
        DURATION_FAKE_VALUE_IF_NOT_SET_IN_ORDER_TO_RANK_LAST = 1000000000
        duration_difference = abs(
            recording.get(
                ApiFields.Names.DURATION_IN_SEC,
                DURATION_FAKE_VALUE_IF_NOT_SET_IN_ORDER_TO_RANK_LAST) - duration_in_sec)
        fields_count = len(recording)
        release_groups_count = len(recording.get(ApiFields.Names.RELEASEGROUPS, []))
        return duration_difference, -fields_count, -release_groups_count

    best_group_of_recordings = max(recordings_grouped_by_score, key=rate_groupe_of_recordings_by_score)
    best_recordings = best_group_of_recordings[ApiFields.Names.RECORDINGS]
    best_recording = min((recording for recording in best_recordings),
                         key=rate_recording_by_similar_duration_and_by_number_of_fields)
    best_recording[ApiFields.Names.SCORE] = \
        best_group_of_recordings[ApiFields.Names.SCORE]
    return best_recording


def get_earliest_release_date_from_musicbrainz_recording_dict(musicbrainz_recording_dict):
    earliest_comparison_date = None
    earliest_release_date = None
    for releasegroup in musicbrainz_recording_dict.get(ApiFields.Names.RELEASEGROUPS, []):
        for release in releasegroup.get(ApiFields.Names.RELEASES, []):
            current_release_date = release.get(ApiFields.Names.DATE, None)
            if current_release_date:
                year = current_release_date.get(ApiFields.Names.YEAR)
                month_or_12 = current_release_date.get(ApiFields.Names.MONTH, 12)
                month_or_1 = current_release_date.get(ApiFields.Names.MONTH, 1)
                _, last_day = monthrange(year, month_or_12)
                day_or_last_of_month = current_release_date.get(ApiFields.Names.DAY, last_day)
                day_or_first = current_release_date.get(ApiFields.Names.DAY, 1)

                comparison_date_obj = datetime.date(year=year, month=month_or_12, day=day_or_last_of_month)

                if not earliest_comparison_date or comparison_date_obj < earliest_comparison_date:
                    earliest_comparison_date = comparison_date_obj
                    earliest_release_date = datetime.date(year=year, month=month_or_1, day=day_or_first)
    return earliest_release_date


def create_musicbrainz_recordinginstance_from_dict(musicbrainz_recording_id: str,
                                                   musicbrainz_recording_dict: dict) -> MusicbrainzRecording:
    musicbrainz_artists_dict = musicbrainz_recording_dict[ApiFields.Names.ARTISTS]
    musicbrainz_artists = []
    for artist_dict in musicbrainz_artists_dict:
        artist, _ = MusicbrainzArtist.objects.get_or_create(
            musicbrainz_id=artist_dict[ApiFields.Names.ID],
            defaults={
                MusicbrainzArtistFields.NAME: artist_dict[ApiFields.Names.NAME],
            })
        musicbrainz_artists.append(artist)

    earliest_release_date = get_earliest_release_date_from_musicbrainz_recording_dict(
        musicbrainz_recording_dict)

    musicbrainz_recording, _ = MusicbrainzRecording.objects.get_or_create(
        musicbrainz_id=musicbrainz_recording_id,
        defaults={MusicbrainzRecordingFields.SCORE: musicbrainz_recording_dict[ApiFields.Names.SCORE],
                  MusicbrainzRecordingFields.TITLE: musicbrainz_recording_dict[ApiFields.Names.TITLE],
                  MusicbrainzRecordingFields.DURATION_IN_SEC: musicbrainz_recording_dict.get(
                      ApiFields.Names.DURATION_IN_SEC, None),
                  MusicbrainzRecordingFields.RELEASE_DATE: earliest_release_date, })
    musicbrainz_recording.musicbrainz_artists.set(musicbrainz_artists)
    return musicbrainz_recording
