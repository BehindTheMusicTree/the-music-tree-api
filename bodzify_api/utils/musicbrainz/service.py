#!/usr/bin/env python

from typing import Optional
import acoustid

from django.core.exceptions import ObjectDoesNotExist

from bodzify_api import settings
from bodzify_api.exception.musicbrainz import ApiErrorMusicbrainzRecordingLookupException, \
    MusicbrainzRecordingLookupException, \
    UnknownErrorMusicbrainzRecordingLookupException, \
    UnknownStatusCodeMusicbrainzRecordingLookupException
from bodzify_api.model.musicbrainz.recording.MusicBrainzRecordingLookupResult import MusicbrainzRecordingLookupResult
from bodzify_api.model.musicbrainz.recording.missing_cause.MusicbrainzRecordingMissingCause \
    import MusicbrainzRecordingMissingCause
from bodzify_api.model.musicbrainz.recording.missing_cause.MusicbrainzRecordingMissingCauseCode \
    import MusicbrainzRecordingMissingCauseCode
from bodzify_api.model.musicbrainz.recording.MusicbrainzRecording import MusicbrainzRecording
from bodzify_api.model.user.User import User
from .utils import ApiFields, get_best_recording_dict_with_score, create_musicbrainz_recordinginstance_from_dict


def get_musicbrainz_best_recording_dict_from_fingerprint_and_duration(fingerprint: bytes,
                                                                      duration_in_sec: float) -> Optional[dict]:
    try:
        lookup = acoustid.lookup(apikey=settings.ACOUSTID_API_KEY,
                                 fingerprint=fingerprint,
                                 duration=duration_in_sec,
                                 meta=['recordings', 'releasegroups', 'releases', 'compress', 'tracks'])

        lookup_status = lookup[ApiFields.Names.STATUS]
        if lookup_status == ApiFields.Values.Status.OK:
            recordings_grouped_by_score = lookup[ApiFields.Names.RESULTS]
            if len(recordings_grouped_by_score) > 0:
                return get_best_recording_dict_with_score(
                    recordings_grouped_by_score=recordings_grouped_by_score, duration_in_sec=duration_in_sec)
            else:
                return None
        elif lookup_status == ApiFields.Values.Status.ERROR:
            error_dict = lookup[ApiFields.Names.ERROR]
            error_code = error_dict[ApiFields.Names.CODE]
            error_message = error_dict[ApiFields.Names.MESSAGE]
            exception_message = f"Error while getting MusicBrainz recording ID: {error_code} - {error_message}"
            raise ApiErrorMusicbrainzRecordingLookupException(exception_message)
        else:
            raise UnknownStatusCodeMusicbrainzRecordingLookupException(lookup_status)
    except Exception as exception:
        raise UnknownErrorMusicbrainzRecordingLookupException(str(exception))


def get_musicbrainz_recording_lookup_result(
        user: User, fingerprint: bytes, duration_in_sec: float) -> MusicbrainzRecordingLookupResult:
    musicbrainz_recording = None
    musicbrainz_recording_missing_cause = None
    musicbrainz_recording_missing_cause_code = None

    if duration_in_sec < 1:
        musicbrainz_recording_missing_cause_code = MusicbrainzRecordingMissingCauseCode.Codes.DURATION_BELOW_1_SEC
        musicbrainz_recording_missing_cause_message = None
    else:
        try:
            musicbrainz_recording_dict = get_musicbrainz_best_recording_dict_from_fingerprint_and_duration(
                fingerprint=fingerprint, duration_in_sec=duration_in_sec)
            if not musicbrainz_recording_dict:
                musicbrainz_recording_missing_cause_code = \
                    MusicbrainzRecordingMissingCauseCode.Codes.LOOKUP_FOUND_NO_MATCHING_RECORDING
                musicbrainz_recording_missing_cause_message = None
            else:
                musicbrainz_recording_id = musicbrainz_recording_dict[ApiFields.Names.ID]
                try:
                    musicbrainz_recording = MusicbrainzRecording.objects.get(musicbrainz_id=musicbrainz_recording_id)
                except ObjectDoesNotExist:
                    musicbrainz_recording = create_musicbrainz_recordinginstance_from_dict(
                        musicbrainz_recording_id=musicbrainz_recording_id,
                        musicbrainz_recording_dict=musicbrainz_recording_dict)

        except MusicbrainzRecordingLookupException as e:
            exception_mapping: dict[type, MusicbrainzRecordingMissingCauseCode.Codes] = {
                ApiErrorMusicbrainzRecordingLookupException:
                    MusicbrainzRecordingMissingCauseCode.Codes.LOOKUP_FAILED_WITH_RESPONSE_ERROR_CODE,
                UnknownStatusCodeMusicbrainzRecordingLookupException:
                    MusicbrainzRecordingMissingCauseCode.Codes.LOOKUP_FAILED_WITH_RESPONSE_UNKNOWN_STATUS_CODE,
                UnknownErrorMusicbrainzRecordingLookupException:
                    MusicbrainzRecordingMissingCauseCode.Codes.LOOKUP_FAILED_FOR_UNKNOWN_REASON,
            }
            musicbrainz_recording_missing_cause_code = exception_mapping[type(e)]
            musicbrainz_recording_missing_cause_message = str(e)

    if musicbrainz_recording_missing_cause_code:
        musicbrainz_recording_missing_cause = MusicbrainzRecordingMissingCause.objects.create(
            user=user,
            code=musicbrainz_recording_missing_cause_code,
            message=musicbrainz_recording_missing_cause_message)

    return MusicbrainzRecordingLookupResult(recording=musicbrainz_recording,
                                            missing_cause=musicbrainz_recording_missing_cause)
