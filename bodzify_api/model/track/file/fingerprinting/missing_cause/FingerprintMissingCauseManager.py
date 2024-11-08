from bodzify_api.model.public_standard_resource.PublicStandardResourceManager \
    import PublicStandardResourceManager


class FingerprintMissingCauseManager(PublicStandardResourceManager):

    def create(self, *args, **kwargs):
        from bodzify_api.model.track.file.fingerprinting.missing_cause.FingerprintMissingCause import Fields
        from bodzify_api.model.track.file.fingerprinting.missing_cause.code.FingerprintMissingCauseCode \
            import FingerprintMissingCauseCode

        code = kwargs.pop(Fields.CODE, None)
        if code is None:
            raise ValueError("The code parameter must be provided when creating an entry.")

        fingerprint_missing_cause_code = FingerprintMissingCauseCode.objects.get(code=code)
        kwargs[Fields.CODE] = fingerprint_missing_cause_code

        return super().create(*args, **kwargs)
