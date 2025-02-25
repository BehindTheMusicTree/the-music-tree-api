
from dataclasses import dataclass

from bodzify_api.model.musicbrainz_resource.children.recording.missing_cause.MusicbrainzRecordingMissingCause import     MusicbrainzRecordingMissingCause
from bodzify_api.model.musicbrainz_resource.children.recording.MusicbrainzRecording import     MusicbrainzRecording


@dataclass
class MusicbrainzRecordingLookupResult:
    _recording: MusicbrainzRecording | None = None
    _missing_cause: MusicbrainzRecordingMissingCause | None = None

    class Meta:
        verbose_name = 'MusicBrainz Recording Lookup Result'
        verbose_name_plural = 'MusicBrainz Recording Lookup Results'

    def __init__(self, recording: MusicbrainzRecording | None,
                 missing_cause: MusicbrainzRecordingMissingCause | None):
        self._recording = recording
        self._missing_cause = missing_cause

    @property
    def is_success(self) -> bool:
        return self._recording is not None

    @property
    def recording(self) -> MusicbrainzRecording:
        if self._recording is None:
            raise ValueError(f"{self.__class__} is not successful")
        return self._recording

    @property
    def missing_cause(self) -> MusicbrainzRecordingMissingCause:
        if self._missing_cause is None:
            raise ValueError(f"{self.__class__} is successful, no missing cause available")
        return self._missing_cause
