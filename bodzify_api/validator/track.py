from django.core.exceptions import ValidationError

import bodzify_api.settings as settings


def track_size(value):  # add this to some file where you can import it from
    limit = settings.TRACK_SIZE_LIMIT_IN_MO * 1000000
    if value.size > limit:
        trackSizeErrorTooLargeMessage = 'File too large. Size should not exceed {size:.3f} Mo.'
        raise ValidationError(trackSizeErrorTooLargeMessage.format(
            size=settings.TRACK_SIZE_LIMIT_IN_MO))
