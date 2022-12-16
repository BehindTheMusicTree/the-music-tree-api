from django import forms
from django.core.validators import FileExtensionValidator

from bodzify_api.validator.LibraryTrackSizeValidator import trackSize
from upload_validator import FileTypeValidator


class UploadTrackForm(forms.Form):
    file = forms.FileField(
        help_text="Only audio formats accepted",  
        validators=[
            FileExtensionValidator(['flac', 'wav', 'mp3']), 
            FileTypeValidator(allowed_types=[ 'audio/*']),
            trackSize
        ]
    )