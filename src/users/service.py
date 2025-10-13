# Fichier : src/users/service.py
from typing import List, Optional
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404, redirect, render

from .models import User, Company


def list_users() -> List[User]:
    """Retourne la liste de tous les utilisateurs."""
    return User.objects.all()


def get_user(user_id: int) -> Optional[User]:
    """Récupère un utilisateur par son ID."""
    return User.objects.filter(id=user_id).first()


def create_user(data: dict) -> User:
    """Crée un nouvel utilisateur dans la base de données."""
    user = User.objects.create(
        username=data['username'],
        email=data.get('email'),
        is_admin=data.get("is_admin", False),
    )
    user.set_password(data["password"])  # 🔒 Sécurisé
    user.save()
    return user

    # On ajoute les compagnies si elles sont fournies
    if 'companies' in data:
        companies = Company.objects.filter(id__in=data['companies'])
        new_user.companies.set(companies)

    return new_user


def update_user(user_id: int, data: dict) -> Optional[User]:
    """Met à jour un utilisateur."""
    user = get_user(user_id)
    if user:
        user.username = data['username']
        user.email = data.get('email')
        user.save()
    return user



def delete_user(user_id: int) -> bool:
    """Supprime un utilisateur."""
    user = get_user(user_id)
    if user:
        user.delete()
        return True
    return False

