
from django.core.files.base import File as DjangoFile

from bodzify_api.model.track.file.fingerprinting.FingerprintingResult import FingerprintingResult
from bodzify_api.model.track.file.fingerprinting.missing_cause.code.FingerprintMissingCauseCode import (
    FingerprintMissingCauseCode
)
from bodzify_api.model.track.file.fingerprinting.missing_cause.FingerprintMissingCause import FingerprintMissingCause
from bodzify_api.model.user.User import User

from . import utils
from .utils import exception as audio_fingerprinter_exc


def _get_fingerprint_and_duration_from_file(user_id: str, file, title: str) -> tuple[bytes, int]:
    from bodzify_api.utils.AudioFile import AudioFile
    filename = AudioFile(file).get_file_name_system()
    fingerprint, duration_in_sec = utils.post_fingerprint_audio(filename=filename, title=title, user_id=user_id)
    return fingerprint, int(duration_in_sec)


def get_fingerprinting_result(user: User, track_file: DjangoFile, title: str) -> FingerprintingResult:

    duration_in_sec = None
    fingerprint = None
    fingerprint_missing_cause = None
    try:
        fingerprint, duration_in_sec = _get_fingerprint_and_duration_from_file(
            user_id=user.pk, file=track_file, title=title)

    except audio_fingerprinter_exc.AudioFingerprinterException as e:
        fingerprint = None
        error_mapping = {
            audio_fingerprinter_exc.WrongFileExtension: FingerprintMissingCauseCode.Codes.WRONG_FILE_EXTENSION,
            audio_fingerprinter_exc.WrongFileType: FingerprintMissingCauseCode.Codes.WRONG_FILE_TYPE,
            audio_fingerprinter_exc.FileNotInPool: FingerprintMissingCauseCode.Codes.FILE_NOT_FOUND_IN_POOL,
            audio_fingerprinter_exc.BadRequestException: FingerprintMissingCauseCode.Codes.UNKNOWN_BAD_REQUEST,
            audio_fingerprinter_exc.InternalServerException: FingerprintMissingCauseCode.Codes.INTERNAL_ERROR,
            audio_fingerprinter_exc.TimeoutException: FingerprintMissingCauseCode.Codes.TIMEOUT_ERROR,
            audio_fingerprinter_exc.FpcalcStatusException: FingerprintMissingCauseCode.Codes.FPCALC_ERROR_WITH_STATUS_2,
            audio_fingerprinter_exc.UnknownUnprocessableEntityException:
            FingerprintMissingCauseCode.Codes.UNKNOWN_UNPROCESSABLE_ENTITY_ERROR,
            audio_fingerprinter_exc.ServiceNotFoundException: FingerprintMissingCauseCode.Codes.SERVICE_NOT_FOUND,
            audio_fingerprinter_exc.ConnectionException: FingerprintMissingCauseCode.Codes.UNKNOWN_CONNEXION_ERROR
        }

        fingerprinting_missing_cause_code = error_mapping.get(e.__class__, None)

        fingerprint_missing_cause = FingerprintMissingCause.objects.create(
            user=user, code=fingerprinting_missing_cause_code, message=e.message)

    return FingerprintingResult(
        fingerprint=fingerprint, duration_in_sec=duration_in_sec, error=fingerprint_missing_cause)
