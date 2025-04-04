"""
Spotify models for Bodzify API
"""
from bodzify_api.model.spotify.SpotifyResource import SpotifyResource
from bodzify_api.model.spotify.children.artist.SpotifyArtist import SpotifyArtist

# Make SpotifyArtist visible at the module level for Django's model discovery
__all__ = ['SpotifyResource', 'SpotifyArtist']
