from django import forms

from upload_validator import FileTypeValidator

from bodzify_api.validator.track import track_size


class UploadTrackForm(forms.Form):
    file = forms.FileField(
        help_text="Only audio formats accepted", 
        validators=[FileTypeValidator(allowed_types=[ 'audio/*']), track_size]
    )