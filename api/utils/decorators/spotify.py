from functools import wraps
from rest_framework.response import Response
from rest_framework import status

from api.model.user.spotify.SpotifyUser import SpotifyUser


def spotify_user_required(view_func):
    """
    Decorator for view methods that require a SpotifyUser.

    This decorator:
    1. Checks if the request.user is authenticated
    2. Attempts to retrieve the matching SpotifyUser
    3. Casts request.user to SpotifyUser for the view function's use

    Usage:
        @spotify_user_required
        def view_method(self, request, ...):
            # request.user is guaranteed to be a SpotifyUser here
    """
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required to access this resource'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            # Check if the user exists in spotify_user table
            spotify_user = SpotifyUser.objects.get(pk=request.user.pk)
            # Cast the user to SpotifyUser for this request
            request.user = spotify_user
            print(f"User cast to SpotifyUser in decorator: {spotify_user.pk}")
        except SpotifyUser.DoesNotExist:
            return Response(
                {'error': 'This resource requires Spotify authorization'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Call the original view function with the SpotifyUser
        return view_func(self, request, *args, **kwargs)

    return wrapper
