import os
import tempfile

from django.db.models.fields.files import FieldFile

from bodzify_api.model.user.User import User
from django.core.files.base import File as DjangoFile
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from bodzify_api import settings
from bodzify_api.model.track.file.fingerprinting.missing_cause.FingerprintMissingCause import FingerprintMissingCause
from bodzify_api.model.track.file.fingerprinting.missing_cause.code.FingerprintMissingCauseCode import FingerprintMissingCauseCode
from bodzify_api.model.track.file.fingerprinting.FingerprintingResult import FingerprintingResult
from bodzify_api.utils.app_django_file import AppDjangoFile
from .utils import error as audio_fingerprinter_error
from . import utils


def _get_fingerprint_and_duration_from_file(user_id: str, file, title: str) -> tuple[bytes, int]:
    if isinstance(file, InMemoryUploadedFile):
        with tempfile.NamedTemporaryFile(delete=False, dir=settings.FILE_UPLOAD_TEMP_DIR) as tmp_file:
            for chunk in file.chunks():
                tmp_file.write(chunk)
            file_path = tmp_file.name
            filename = os.path.basename(file_path)
            fingerprint, duration_in_sec = utils.post_fingerprint_audio(user_id=user_id,
                                                                        filename=filename,
                                                                        title=title,)
            os.remove(file_path)
    elif isinstance(file, TemporaryUploadedFile):
        file_path = file.file.name
        filename = os.path.basename(file_path)
        fingerprint, duration_in_sec = utils.post_fingerprint_audio(user_id=user_id,
                                                                    filename=filename,
                                                                    title=title)
    elif isinstance(file, AppDjangoFile):
        filename = os.path.basename(file.file_abs_path)
        fingerprint, duration_in_sec = utils.post_fingerprint_audio(user_id=user_id,
                                                                    filename=filename,
                                                                    title=title)
    elif isinstance(file, FieldFile):
        file_path = file.path
        filename = os.path.basename(file_path)
        fingerprint, duration_in_sec = utils.post_fingerprint_audio(user_id=user_id,
                                                                    filename=filename,
                                                                    title=title)
    else:
        raise ValueError(f"Unsupported file type {type(file)}")

    return fingerprint, int(duration_in_sec)


def get_fingerprinting_result(user: User, track_file: DjangoFile, title: str) -> FingerprintingResult:

    duration_in_sec = None
    fingerprint = None
    fingerprint_missing_cause = None
    try:
        fingerprint, duration_in_sec = _get_fingerprint_and_duration_from_file(user_id=user.pk,
                                                                               file=track_file,
                                                                               title=title)

    except audio_fingerprinter_error.AudioFingerprinterError as e:
        fingerprint = None
        error_mapping: [type, FingerprintMissingCauseCode.Codes] = {
            audio_fingerprinter_error.WrongFileExtension: FingerprintMissingCauseCode.Codes.WRONG_FILE_EXTENSION,
            audio_fingerprinter_error.WrongFileType: FingerprintMissingCauseCode.Codes.WRONG_FILE_TYPE,
            audio_fingerprinter_error.FileNotInPool: FingerprintMissingCauseCode.Codes.FILE_NOT_FOUND_IN_POOL,
            audio_fingerprinter_error.BadRequestError: FingerprintMissingCauseCode.Codes.UNKNOWN_BAD_REQUEST,
            audio_fingerprinter_error.InternalServerError: FingerprintMissingCauseCode.Codes.INTERNAL_ERROR,
            audio_fingerprinter_error.TimeoutError: FingerprintMissingCauseCode.Codes.TIMEOUT_ERROR,
            audio_fingerprinter_error.FpcalcStatusError:
            FingerprintMissingCauseCode.Codes.FPCALC_ERROR_WITH_STATUS_2,
            audio_fingerprinter_error.UnknownUnprocessableEntityError:
            FingerprintMissingCauseCode.Codes.UNKNOWN_UNPROCESSABLE_ENTITY_ERROR,
            audio_fingerprinter_error.ServiceNotFoundError: FingerprintMissingCauseCode.Codes.SERVICE_NOT_FOUND,
            audio_fingerprinter_error.ConnectionError: FingerprintMissingCauseCode.Codes.UNKNOWN_CONNEXION_ERROR,
        }

        fingerprinting_missing_cause_code = error_mapping.get(e.__class__, None)

        fingerprint_missing_cause = FingerprintMissingCause.objects.create(user=user,
                                                                           code=fingerprinting_missing_cause_code,
                                                                           message=str(e))

    return FingerprintingResult(fingerprint=fingerprint,
                                duration_in_sec=duration_in_sec,
                                error=fingerprint_missing_cause)
