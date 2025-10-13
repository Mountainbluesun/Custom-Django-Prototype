# Fichier : src/catalog/models.py
from django.db import models
from companies.models import Company  # On importe le modèle Company


class Product(models.Model):
    # Champs de base
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100, unique=True)
    threshold = models.IntegerField(default=0)

    # Le lien vers l'entreprise
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.sku})"