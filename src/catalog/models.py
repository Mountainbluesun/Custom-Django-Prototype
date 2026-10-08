from django.db import models
from companies.models import Company  # Import the Company model


class Product(models.Model):
    # Basic fields
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100, unique=True)
    threshold = models.IntegerField(default=0)

    # Link to the company
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.sku})"