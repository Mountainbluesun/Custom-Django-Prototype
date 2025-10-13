from django.contrib.auth.models import AbstractUser
from django.db import models
from companies.models import Company

class User(AbstractUser):
    """
    Modèle utilisateur personnalisé basé sur Django.
    On hérite d'AbstractUser pour profiter de tous les mécanismes
    d'authentification, de hashing de mot de passe, permissions, etc.
    """

    # Ajouter un champ is_admin si nécessaire (facultatif car AbstractUser a is_staff et is_superuser)
    is_admin = models.BooleanField(default=True)

    # Lien vers les entreprises
    companies = models.ManyToManyField(Company, blank=True)
    # On peut ajouter d'autres champs personnalisés ici si besoin
    # exemple : reset_token si tu veux gérer des tokens custom
    reset_token = models.CharField(max_length=64, blank=True, null=True)

    # Champ temporaire pour récupérer l'ancien hash
    old_password_hash = models.CharField(max_length=128, blank=True, null=True)


    def __str__(self):
        return self.username



