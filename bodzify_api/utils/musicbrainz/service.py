

import acoustid
from acoustid import WebServiceError
from django.core.exceptions import ObjectDoesNotExist

from bodzify_api import settings
from bodzify_api.exception import musicbrainz as musicbrainz_exception
from bodzify_api.model.musicbrainz_resource.children.recording.missing_cause.code.MusicbrainzRecordingMissingCauseCode import (
    MusicbrainzRecordingMissingCauseCode
)
from bodzify_api.model.musicbrainz_resource.children.recording.missing_cause.MusicbrainzRecordingMissingCause import (
    MusicbrainzRecordingMissingCause
)
from bodzify_api.model.musicbrainz_resource.children.recording.MusicbrainzRecording import MusicbrainzRecording
from bodzify_api.model.musicbrainz_resource.children.recording.MusicBrainzRecordingLookupResult import (
    MusicbrainzRecordingLookupResult
)
from bodzify_api.model.user.User import User

from . import utils
from .ApiFields import ApiFields
from .LookupMetaFields import LookupMetaFields


def _get_musicbrainz_best_recording_dict_from_fingerprint_and_duration(fingerprint: bytes,
                                                                       duration_in_sec: float) -> dict | None:
    try:
        lookup = acoustid.lookup(apikey=settings.ACOUSTID_API_KEY,
                                 fingerprint=fingerprint,
                                 duration=duration_in_sec,
                                 meta=[LookupMetaFields.RECORDINGS,
                                       LookupMetaFields.RELEASE_GROUPS,
                                       LookupMetaFields.RELEASES,
                                       LookupMetaFields.COMPRESS,
                                       LookupMetaFields.TRACKS])

        lookup_status = lookup[ApiFields.Names.STATUS]
        if lookup_status == ApiFields.Values.Status.OK:
            recordings_grouped_by_score = lookup[ApiFields.Names.RESULTS]
            if len(recordings_grouped_by_score) > 0:
                return utils.get_best_recording_dict_with_score(recordings_grouped_by_score=recordings_grouped_by_score,
                                                                duration_in_sec=duration_in_sec)
            else:
                return None
        elif lookup_status == ApiFields.Values.Status.ERROR:
            error_dict = lookup[ApiFields.Names.ERROR]
            error_code = error_dict[ApiFields.Names.CODE]
            error_message = error_dict[ApiFields.Names.MESSAGE]
            if error_code == 3:
                raise musicbrainz_exception.InvalidFingerprintMusicbrainzRecordingLookupException(
                    f"Musicbrainz original lookup error message: \"{error_message}\"")
            elif error_code == 5:
                raise musicbrainz_exception.InternalErrorMusicbrainzRecordingLookupException(
                    f"Musicbrainz original lookup error message: \"{error_message}\"")
            else:
                exception_message = f"Error while getting MusicBrainz recording ID: {error_code} - {error_message}"
                raise musicbrainz_exception.UnknownErrorCodeMusicbrainzRecordingLookupException(exception_message)
        else:
            raise musicbrainz_exception.UnknownStatusMusicbrainzRecordingLookupException(lookup_status)
    except Exception as exception:
        if isinstance(exception, musicbrainz_exception.MusicbrainzRecordingLookupException):
            raise exception
        if isinstance(exception, WebServiceError):
            raise musicbrainz_exception.DNSResolutionErrorMusicbrainzRecordingLookupException(str(exception))
        raise musicbrainz_exception.UnknownErrorCodeMusicbrainzRecordingLookupException(str(exception))


def get_musicbrainz_recording_lookup_result(user: User,
                                            fingerprint: bytes,
                                            duration_in_sec: float) -> MusicbrainzRecordingLookupResult:
    musicbrainz_recording = None
    musicbrainz_recording_missing_cause = None
    musicbrainz_recording_missing_cause_code = None

    if duration_in_sec <= 1:
        musicbrainz_recording_missing_cause_code = MusicbrainzRecordingMissingCauseCode.Codes.DURATION_BELOW_OR_EQUAL_1_SEC
        musicbrainz_recording_missing_cause_message = None
    else:
        try:
            musicbrainz_recording_dict = _get_musicbrainz_best_recording_dict_from_fingerprint_and_duration(
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
                    musicbrainz_recording = utils.create_musicbrainz_recording_instance_from_dict(
                        musicbrainz_recording_id=musicbrainz_recording_id,
                        musicbrainz_recording_dict=musicbrainz_recording_dict)

        except musicbrainz_exception.MusicbrainzRecordingLookupException as e:
            exception_mapping: dict[type, MusicbrainzRecordingMissingCauseCode.Codes] = {
                musicbrainz_exception.InvalidFingerprintMusicbrainzRecordingLookupException:
                    MusicbrainzRecordingMissingCauseCode.Codes.LOOKUP_FAILED_DUE_TO_INVALID_FINGERPRINT,
                musicbrainz_exception.InternalErrorMusicbrainzRecordingLookupException:
                    MusicbrainzRecordingMissingCauseCode.Codes.LOOKUP_FAILED_WITH_INTERNAL_ERROR,
                musicbrainz_exception.UnknownErrorCodeMusicbrainzRecordingLookupException:
                    MusicbrainzRecordingMissingCauseCode.Codes.LOOKUP_FAILED_WITH_UNKNOWN_RESPONSE_ERROR_CODE,
                musicbrainz_exception.UnknownStatusMusicbrainzRecordingLookupException:
                    MusicbrainzRecordingMissingCauseCode.Codes.LOOKUP_FAILED_WITH_UNKNOWN_RESPONSE_STATUS_CODE,
                musicbrainz_exception.DNSResolutionErrorMusicbrainzRecordingLookupException:
                    MusicbrainzRecordingMissingCauseCode.Codes.LOOKUP_FAILED_DNS_RESOLUTION_ERROR}
            musicbrainz_recording_missing_cause_code = exception_mapping[type(e)]
            error_message = str(e)
            if len(error_message) > settings.MUSICBRAINZ_RECORDING_MISSING_CAUSE_MESSAGE_LEN_MAX:
                musicbrainz_recording_missing_cause_message = error_message[
                    :settings.MUSICBRAINZ_RECORDING_MISSING_CAUSE_MESSAGE_LEN_MAX - 3] + "..."
            else:
                musicbrainz_recording_missing_cause_message = error_message

    if musicbrainz_recording_missing_cause_code:
        musicbrainz_recording_missing_cause = MusicbrainzRecordingMissingCause.objects.create(
            user=user,
            code=musicbrainz_recording_missing_cause_code,
            message=musicbrainz_recording_missing_cause_message)

    return MusicbrainzRecordingLookupResult(recording=musicbrainz_recording,
                                            missing_cause=musicbrainz_recording_missing_cause)
