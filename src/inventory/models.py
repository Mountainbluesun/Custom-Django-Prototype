# Fichier : src/inventory/models.py
from django.db import models
from catalog.models import Product
from companies.models import Company
from users.models import User


class Movement(models.Model):
    # Les liens vers les autres tables
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Les informations sur le mouvement
    quantity = models.IntegerField()
    kind = models.CharField(max_length=20)  # 'IN', 'OUT', 'TRANSFER_IN', 'TRANSFER_OUT'
    note = models.TextField(blank=True, null=True)

    # La date du mouvement
    timestamp = models.DateTimeField(auto_now_add=True)  # Ajoute la date et l'heure automatiquement

    def __str__(self):
        return f"{self.kind} - {self.quantity} x {self.product.name}"