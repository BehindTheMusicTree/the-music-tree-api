from rest_framework import serializers

from bodzify_api.model.track.file.fingerprinting.missing_cause.code.FingerprintMissingCauseCode \
    import FingerprintMissingCauseCode
from .Fields import Fields


class FingerprintMissingCauseCodeDetailedSerializer(serializers.ModelSerializer):

    class Meta:
        model = FingerprintMissingCauseCode
        fields = [Fields.CODE, Fields.LABEL]
