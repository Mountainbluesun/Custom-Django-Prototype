from django.contrib.auth.models import AbstractUser
from django.db import models
from companies.models import Company

class User(AbstractUser):
    """
    Custom user model based on Django.
    We inherit from AbstractUser to benefit from all the built-in
    authentication mechanisms, password hashing, permissions, etc.
    """

    # Add an is_admin field if needed (optional since AbstractUser already has is_staff and is_superuser)
    is_admin = models.BooleanField(default=True)

    # Link to companies
    companies = models.ManyToManyField(Company, blank=True)
    # Other custom fields can be added here if needed
    # example: reset_token if you want to manage custom tokens
    reset_token = models.CharField(max_length=64, blank=True, null=True)

    # Temporary field to recover the old hash
    old_password_hash = models.CharField(max_length=128, blank=True, null=True)


    def __str__(self):
        return self.username