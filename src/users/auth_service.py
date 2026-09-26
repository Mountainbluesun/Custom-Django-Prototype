from typing import Optional
from django.contrib.auth.hashers import check_password
from .models import User


def authenticate(username: str, password: str) -> Optional[User]:
    """
    Returns the User object if the credentials are valid, otherwise None.
    """
    # Look up the user in the database
    user = User.objects.filter(username=username).first()

    # Check that the user exists and the password is correct
    if user and check_password(password, user.password_hash):
        return user

    return None