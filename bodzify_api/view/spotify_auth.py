from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.contrib.auth import login

from bodzify_api.utils.spotify_api.oauth import SpotifyOAuthService
from bodzify_api.model.user.spotify.SpotifyUser import SpotifyUser
from bodzify_api.utils.jwt import create_jwt_token
from bodzify_api.model.user.Fields import Fields
from bodzify_api.model.spotify_resource.Fields import Fields as SpotifyFields
from bodzify_api.utils.spotify_api.SpotifyClient import SpotifyAPIService
from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode

spotify_service = SpotifyAPIService()


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
        'accessToken': jwt_token,
        'user': {
            'spotify_profile': user.spotify_profile,
            Fields.ID: user.id,
            Fields.EMAIL: user.email,
            SpotifyFields.SPOTIFY_ID: user.spotify_id,
            'display_name': user.spotify_profile.get('display_name'),
            'external_urls': user.spotify_profile.get('external_urls'),
            'followers': user.spotify_profile.get('followers'),
            'href': user.spotify_profile.get('href'),
            'images': user.spotify_profile.get('images'),
            'type': user.spotify_profile.get('type'),
            'uri': user.spotify_profile.get('uri')
        }
    })


@api_view(['GET'])
def spotify_callback(request):
    """
    Handle the Spotify OAuth callback
    """
    try:
        code = request.GET.get('code')
        if not code:
            return Response(
                {'error': 'Authorization code is required'},
                status=status.HTTP_400_BAD_REQUEST
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
            'accessToken': jwt_token,
            'user': {
                'spotify_profile': user.spotify_profile,
                Fields.ID: user.id,
                Fields.EMAIL: user.email,
                SpotifyFields.SPOTIFY_ID: user.spotify_id,
                'display_name': user.spotify_profile.get('display_name'),
                'external_urls': user.spotify_profile.get('external_urls'),
                'followers': user.spotify_profile.get('followers'),
                'href': user.spotify_profile.get('href'),
                'images': user.spotify_profile.get('images'),
                'type': user.spotify_profile.get('type'),
                'uri': user.spotify_profile.get('uri')
            }
        })

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
