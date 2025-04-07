from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone

from bodzify_api.utils.spotify.oauth import SpotifyOAuthService
from bodzify_api.model.user.SpotifyUser import SpotifyUser
from bodzify_api.utils.jwt import create_jwt_token
from bodzify_api.model.user.Fields import Fields
from bodzify_api.model.spotify.Fields import Fields as SpotifyFields
from bodzify_api.utils.spotify.service import SpotifyAPIService

spotify_service = SpotifyAPIService()


@api_view(['POST'])
@permission_classes([AllowAny])
def spotify_auth(request):
    """
    Handle Spotify authentication code from frontend
    """
    print("\n=== Spotify Auth Called ===")
    code = request.data.get('code')
    if not code:
        return Response({'error': 'No code provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        oauth_service = SpotifyOAuthService()

        # Get access token
        token_info = oauth_service.get_access_token(code)
        access_token = token_info['access_token']
        refresh_token = token_info['refresh_token']

        # Get user info
        user_info = oauth_service.get_user_info(access_token)
        print(f"User info: {user_info}")

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

        print(f"User authenticated: {user.username}")

        # Create JWT token
        jwt_token = create_jwt_token(user)

        print("Auth complete.")
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
        print(f"Auth error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def spotify_callback(request):
    """
    Handle the Spotify OAuth callback
    """
    code = request.GET.get('code')
    if not code:
        return Response(
            {'error': 'Authorization code is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
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
