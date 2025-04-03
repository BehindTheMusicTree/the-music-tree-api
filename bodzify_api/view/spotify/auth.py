from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from bodzify_api.utils.spotify.oauth import SpotifyOAuthService
from bodzify_api.model.user.User import User
from bodzify_api.utils.jwt import create_jwt_token


@api_view(['GET'])
def spotify_auth(request):
    """
    Get the Spotify authorization URL
    """
    oauth_service = SpotifyOAuthService()
    auth_url = oauth_service.get_auth_url()
    return Response({'auth_url': auth_url})


@api_view(['POST'])
def spotify_auth_api(request):
    """
    Handle Spotify authentication code from frontend
    This endpoint matches what the frontend expects when exchanging the auth code
    """
    # Extract code from request body instead of query parameters
    code = request.data.get('code')

    if not code:
        return Response(
            {'error': 'Authorization code is required in request body'},
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

        # Create or update user
        user, created = User.objects.get_or_create(
            spotify_id=spotify_id,
            defaults={
                'email': email,
                'spotify_access_token': access_token,
                'spotify_refresh_token': refresh_token
            }
        )

        if not created:
            # Update tokens for existing user
            user.spotify_access_token = access_token
            user.spotify_refresh_token = refresh_token
            user.save()

        # Create JWT token
        jwt_token = create_jwt_token(user)

        return Response({
            'token': jwt_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'spotify_id': user.spotify_id
            }
        })

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


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

        # Create or update user
        user, created = User.objects.get_or_create(
            spotify_id=spotify_id,
            defaults={
                'email': email,
                'spotify_access_token': access_token,
                'spotify_refresh_token': refresh_token
            }
        )

        if not created:
            # Update tokens for existing user
            user.spotify_access_token = access_token
            user.spotify_refresh_token = refresh_token
            user.save()

        # Create JWT token
        jwt_token = create_jwt_token(user)

        return Response({
            'token': jwt_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'spotify_id': user.spotify_id
            }
        })

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
