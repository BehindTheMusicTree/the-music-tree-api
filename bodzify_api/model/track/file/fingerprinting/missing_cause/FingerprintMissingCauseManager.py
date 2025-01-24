from bodzify_api.model.public_standard_resource.StandardResourceManager import StandardResourceManager
from .Fields import Fields


class FingerprintMissingCauseManager(StandardResourceManager):

    def create(self, *args, **kwargs):
        from .code.FingerprintMissingCauseCode import FingerprintMissingCauseCode

        code = kwargs.pop(Fields.CODE, None)
        if code is None:
            raise ValueError("The code parameter must be provided when creating an entry.")

        fingerprint_missing_cause_code = FingerprintMissingCauseCode.objects.get(code=code)
        kwargs[Fields.CODE] = fingerprint_missing_cause_code

        return super().create(*args, **kwargs)
