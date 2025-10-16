from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from companies.models import Company


class UserManager(BaseUserManager):
    """
    Manager personnalisé pour le modèle User.
    Gère la création des utilisateurs normaux et superutilisateurs.
    """

    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Crée et sauvegarde un utilisateur normal.
        is_admin=True par défaut (selon votre logique métier).
        """
        if not username:
            raise ValueError("Le nom d'utilisateur est obligatoire")

        email = self.normalize_email(email) if email else None

        # Valeurs par défaut
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Hash le mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Crée et sauvegarde un superutilisateur.
        Force is_staff, is_superuser et is_admin à True.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Un superutilisateur doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Un superutilisateur doit avoir is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé basé sur Django.
    On hérite d'AbstractUser pour profiter de tous les mécanismes
    d'authentification, de hashing de mot de passe, permissions, etc.
    """

    # Ajouter un champ is_admin si nécessaire (facultatif car AbstractUser a is_staff et is_superuser)
    is_admin = models.BooleanField(default=True)
    # Sûr de toi pour le is admin à True ?

    # Lien vers les entreprises
    companies = models.ManyToManyField(Company, blank=True)
    # On peut ajouter d'autres champs personnalisés ici si besoin
    # exemple : reset_token si tu veux gérer des tokens custom
    reset_token = models.CharField(max_length=64, blank=True, null=True)

    # Champ temporaire pour récupérer l'ancien hash
    old_password_hash = models.CharField(max_length=128, blank=True, null=True)

    # Utiliser le manager personnalisé
    objects = UserManager()

    def __str__(self):
        return self.username



