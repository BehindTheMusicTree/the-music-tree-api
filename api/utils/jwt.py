from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from datetime import datetime, timedelta


def create_jwt_token(user) -> dict:
    """
    Create JWT tokens for the given user

    Args:
        user: The user instance

    Returns:
        Dictionary containing access token, refresh token and expiration time
    """
    refresh = RefreshToken.for_user(user)
    access = AccessToken.for_user(user)
    return {
        'access': str(access),
        'refresh': str(refresh),
        'expires_at': datetime.now() + timedelta(minutes=5)  # Default JWT access token expiration
    }
