
from dataclasses import dataclass
from typing import Optional

from bodzify_api.model.track.file.fingerprinting.missing_cause.FingerprintMissingCause import FingerprintMissingCause


@dataclass
class FingerprintingResult:
    _fingerprint: Optional[bytes] = None
    _duration_in_sec: Optional[int] = None
    _error: Optional[FingerprintMissingCause] = None

    def __init__(self, fingerprint: Optional[bytes],
                 duration_in_sec: Optional[int],
                 error: Optional[FingerprintMissingCause]):
        self._fingerprint = fingerprint
        self._duration_in_sec = duration_in_sec
        self._error = error

    @property
    def is_success(self) -> bool:
        return self._fingerprint is not None

    @property
    def fingerprint(self) -> bytes:
        if self._fingerprint is None:
            raise ValueError(f"{self.__class__} is not successful")
        return self._fingerprint

    @property
    def duration_in_sec(self) -> int:
        if self._duration_in_sec is None:
            raise ValueError(f"{self.__class__} is not successful")
        return self._duration_in_sec

    @property
    def missing_cause(self) -> FingerprintMissingCause:
        if self._error is None:
            raise ValueError(f"{self.__class__} is successful, no error available")
        return self._error
