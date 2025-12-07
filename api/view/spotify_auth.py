from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.contrib.auth import login

from api.utils.spotify_api.oauth import SpotifyOAuthService
from api.utilsort create_jwt_token
from api.model.user.spotify.SpotifyUser import SpotifyUser
from api.model.user.spotify.Fields import Fields as SpotifyUserFields
from api.model.spotify_resource.Fields import Fields as SpotifyFields
from api.exception.validation.app.AppValidationException import AppValidationException
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode


@api_view(['POST'])
@permission_classes([AllowAny])
def spotify_auth(request):
    """
    Handle Spotify authentication code from frontend
    """
    code = request.data.get('code')
    if not code:
        raise AppValidationException(
            field_name='code',
            message='No code provided',
            field_validation_error_code=FieldValidationErrorCode.REQUIRED
        )

    oauth_service = SpotifyOAuthService()

    # Get access token
    token_info = oauth_service.get_access_token(code)
    access_token = token_info['access_token']
    refresh_token = token_info['refresh_token']

    # Get user info
    user_info = oauth_service.get_user_info(access_token)

    spotify_id = user_info['id']
    email = user_info.get('email')
    display_name = user_info.get('display_name', spotify_id)

    # Create or update user
    user, created = SpotifyUser.objects.get_or_create(
        spotify_id=spotify_id,
        defaults={
            'email': email,
            'username': display_name,
            'spotify_access_token': access_token,
            'spotify_refresh_token': refresh_token,
            'spotify_token_expires_at': timezone.now() + timezone.timedelta(seconds=token_info['expires_in']),
            'spotify_profile': user_info
        }
    )

    if not created:
        # Update tokens and profile for existing user
        user.spotify_access_token = access_token
        user.spotify_refresh_token = refresh_token
        user.spotify_profile = user_info
        user.spotify_token_expires_at = timezone.now() + timezone.timedelta(seconds=token_info['expires_in'])
        user.save()

    # Create JWT token
    jwt_token = create_jwt_token(user)

    login(request, user)
    return Response({
        'accessToken': jwt_token['access'],
        'refreshToken': jwt_token['refresh'],
        'expires_at': jwt_token['expires_at'],
        'spotifyUser': {
            SpotifyUserFields.SPOTIFY_PROFILE: user.spotify_profile,
            SpotifyUserFields.ID: user.id,
            SpotifyUserFields.EMAIL: user.email,
            SpotifyFields.SPOTIFY_ID: user.spotify_id,
            SpotifyUserFields.DISPLAY_NAME: user.spotify_profile.get('display_name'),
            SpotifyUserFields.FOLLOWERS: user.spotify_profile.get('followers'),
            SpotifyUserFields.HREF: user.spotify_profile.get('href'),
            SpotifyUserFields.IMAGES: user.spotify_profile.get('images'),
            SpotifyUserFields.TYPE: user.spotify_profile.get('type'),
            SpotifyUserFields.URI: user.spotify_profile.get('uri')
        }
    })
