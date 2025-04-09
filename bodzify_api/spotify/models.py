"""
Spotify models for Bodzify API
"""
from bodzify_api.model.spotify_resource.SpotifyResource import SpotifyResource
from bodzify_api.model.spotify_resource.children.artist.SpotifyArtist import SpotifyArtist

# Make SpotifyArtist visible at the module level for Django's model discovery
__all__ = ['SpotifyResource', 'SpotifyArtist']
