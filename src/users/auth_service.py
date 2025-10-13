from typing import Optional
from django.contrib.auth.hashers import check_password
from .models import User


def authenticate(username: str, password: str) -> Optional[User]:
    """
    Retourne l'objet User si les identifiants sont valides, sinon None.
    """
    # On cherche l'utilisateur dans la base de données
    user = User.objects.filter(username=username).first()

    # On vérifie si l'utilisateur existe et si le mot de passe est correct
    if user and check_password(password, user.password_hash):
        return user

    return None