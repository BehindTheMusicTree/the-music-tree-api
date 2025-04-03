
from rest_framework_simplejwt.tokens import RefreshToken


def create_jwt_token(user) -> str:
    """
    Create a JWT token for the given user

    Args:
        user: The user instance

    Returns:
        The JWT access token
    """
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
