#!/usr/bin/env python

from django.core.exceptions import ObjectDoesNotExist

from typing import Optional
import acoustid
import datetime
from calendar import monthrange

from bodzify_api import settings
from bodzify_api.exception.musicbrainz import MusicbrainzException
from bodzify_api.model.musicbrainz.MusicbrainzArtist import MusicbrainzArtist, \
    AttributesLabels as MusicBrainzArtistAttributesLabels
from bodzify_api.model.musicbrainz.MusicbrainzRecording import MusicbrainzRecording


class MusicbrainzApiFields:
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
        DATE = 'date'
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


class MusicBrainzService:

    @ staticmethod
    def _get_best_recording_dict_with_score(recordings_grouped_by_score, duration_in_sec):
        def rate_groupe_of_recordings_by_score(group_of_recordings):
            return group_of_recordings[MusicbrainzApiFields.Names.SCORE]

        def rate_recording_by_similar_duration_and_by_number_of_fields(recording):
            DURATION_FAKE_VALUE_IF_NOT_SET_IN_ORDER_TO_RANK_LAST = 1000000000
            duration_difference = abs(
                recording.get(
                    MusicbrainzApiFields.Names.DURATION_IN_SEC,
                    DURATION_FAKE_VALUE_IF_NOT_SET_IN_ORDER_TO_RANK_LAST) - duration_in_sec)
            fields_count = len(recording)
            release_groups_count = len(recording.get(MusicbrainzApiFields.Names.RELEASEGROUPS, []))
            return duration_difference, -fields_count, -release_groups_count

        best_group_of_recordings = max(recordings_grouped_by_score, key=rate_groupe_of_recordings_by_score)
        best_recordings = best_group_of_recordings[MusicbrainzApiFields.Names.RECORDINGS]
        best_recording = min((recording for recording in best_recordings),
                             key=rate_recording_by_similar_duration_and_by_number_of_fields)
        best_recording[MusicbrainzApiFields.Names.SCORE] = best_group_of_recordings[MusicbrainzApiFields.Names.SCORE]
        return best_recording

    @ staticmethod
    def _get_earliest_release_date_from_musicbrainz_recording_dict(musicbrainz_recording_dict):
        earliest_comparison_date = None
        earliest_release_date = None
        for releasegroup in musicbrainz_recording_dict.get(MusicbrainzApiFields.Names.RELEASEGROUPS, []):
            for release in releasegroup.get(MusicbrainzApiFields.Names.RELEASES, []):
                current_release_date = release.get(MusicbrainzApiFields.Names.DATE, None)
                if current_release_date:
                    year = current_release_date.get(MusicbrainzApiFields.Names.YEAR)
                    month_or_12 = current_release_date.get(MusicbrainzApiFields.Names.MONTH, 12)
                    month_or_1 = current_release_date.get(MusicbrainzApiFields.Names.MONTH, 1)
                    _, last_day = monthrange(year, month_or_12)
                    day_or_last_of_month = current_release_date.get(
                        MusicbrainzApiFields.Names.DAY, last_day)
                    day_or_first = current_release_date.get(MusicbrainzApiFields.Names.DAY, 1)

                    comparison_date_obj = datetime.date(year=year, month=month_or_12, day=day_or_last_of_month)

                    if not earliest_comparison_date or comparison_date_obj < earliest_comparison_date:
                        earliest_comparison_date = comparison_date_obj
                        earliest_release_date = datetime.date(year=year, month=month_or_1, day=day_or_first)
        return earliest_release_date

    @staticmethod
    def create_musicbrainz_recording_instance_from_dict(musicbrainz_recording_uuid: str,
                                                        musicbrainz_recording_dict: dict) -> MusicbrainzRecording:
        musicbrainz_artists_dict = musicbrainz_recording_dict[MusicbrainzApiFields.Names.ARTISTS]
        musicbrainz_artists = list()
        for artist_dict in musicbrainz_artists_dict:
            artist, _ = MusicbrainzArtist.objects.get_or_create(
                uuid=artist_dict[MusicbrainzApiFields.Names.ID],
                defaults={
                    MusicBrainzArtistAttributesLabels.NAME: artist_dict[MusicbrainzApiFields.Names.NAME],
                })
            musicbrainz_artists.append(artist)

        earliest_release_date = MusicBrainzService._get_earliest_release_date_from_musicbrainz_recording_dict(
            musicbrainz_recording_dict)

        musicbrainz_recording = MusicbrainzRecording.objects.create(
            uuid=musicbrainz_recording_uuid,
            score=musicbrainz_recording_dict[MusicbrainzApiFields.Names.SCORE],
            title=musicbrainz_recording_dict[MusicbrainzApiFields.Names.TITLE],
            duration_in_sec=musicbrainz_recording_dict[MusicbrainzApiFields.Names.DURATION_IN_SEC],
            release_date=earliest_release_date)
        musicbrainz_recording.musicbrainz_artists.set(musicbrainz_artists)
        return musicbrainz_recording

    @ staticmethod
    def get_musicbrainz_best_recording_dict_from_fingerprint_and_duration(fingerprint: str,
                                                                          duration_in_sec: float) -> Optional[dict]:
        try:
            lookup = acoustid.lookup(apikey=settings.ACOUSTID_API_KEY,
                                     fingerprint=fingerprint,
                                     duration=duration_in_sec,
                                     meta=['recordings', 'releasegroups', 'releases', 'compress', 'tracks'])
            if lookup[MusicbrainzApiFields.Names.STATUS] == MusicbrainzApiFields.Values.Status.OK:
                recordings_grouped_by_score = lookup[MusicbrainzApiFields.Names.RESULTS]
                if len(recordings_grouped_by_score) > 0:
                    return MusicBrainzService._get_best_recording_dict_with_score(
                        recordings_grouped_by_score=recordings_grouped_by_score, duration_in_sec=duration_in_sec)
                else:
                    return None
            elif lookup[MusicbrainzApiFields.Names.STATUS] == MusicbrainzApiFields.Values.Status.ERROR:
                error_dict = lookup[MusicbrainzApiFields.Names.ERROR]
                error_code = error_dict[MusicbrainzApiFields.Names.CODE]
                error_message = error_dict[MusicbrainzApiFields.Names.MESSAGE]
                exception_message = f"Error while getting musicbrainz recording ID: {error_code} - {error_message}"
                raise MusicbrainzException(exception_message)
            else:
                raise MusicbrainzException("Unknown error while getting musicbrainz recording ID")
        except Exception as exception:
            raise MusicbrainzException(str(exception))

    @staticmethod
    def update_data_with_musicbrainz_recording_pk_from_fingerprint_and_duration_if_found(data: dict,
                                                                                         data_recording_key: str,
                                                                                         data_lookup_error_key: str,
                                                                                         fingerprint: bytes,
                                                                                         duration_in_sec: float):
        if duration_in_sec > 0:  # If the duration is 0, it is not possible to get a musicbrainz recording
            try:
                musicbrainz_recording_dict = MusicBrainzService.get_musicbrainz_best_recording_dict_from_fingerprint_and_duration(
                    fingerprint=fingerprint, duration_in_sec=duration_in_sec)  # type: ignore
                if musicbrainz_recording_dict:
                    musicbrainz_recording_uuid = musicbrainz_recording_dict[MusicbrainzApiFields.Names.ID]
                    try:
                        musicbrainz_recording_pk = MusicbrainzRecording.objects.get(uuid=musicbrainz_recording_uuid).pk
                    except ObjectDoesNotExist:
                        musicbrainz_recording = MusicBrainzService._create_musicbrainz_recording_instance_from_dict(
                            musicbrainz_recording_uuid=musicbrainz_recording_uuid,
                            musicbrainz_recording_dict=musicbrainz_recording_dict)
                        musicbrainz_recording_pk = musicbrainz_recording.pk

                    data[data_recording_key] = musicbrainz_recording_pk
                data[data_lookup_error_key] = None

            except MusicbrainzException as e:
                data[data_lookup_error_key] = str(e)
