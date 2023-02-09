from django import forms
from django.forms import ModelForm

from bodzify_api.model.track.LibraryTrack import LibraryTrack


class TrackPutForm(ModelForm):
    artistName = forms.CharField(max_length=100)
    albumName = forms.CharField(max_length=100)

    class Meta:
        model = LibraryTrack
        fields = ['title', 'artistName', 'albumName', 'genre', 'rating', 'language']
