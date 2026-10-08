from django.db import models
from catalog.models import Product
from companies.models import Company
from users.models import User


class Movement(models.Model):
    # Links to the other tables
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Information about the movement
    quantity = models.IntegerField()
    kind = models.CharField(max_length=20)  # 'IN', 'OUT', 'TRANSFER_IN', 'TRANSFER_OUT'
    note = models.TextField(blank=True, null=True)

    # Date of the movement
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically adds the date and time

    def __str__(self):
        return f"{self.kind} - {self.quantity} x {self.product.name}"