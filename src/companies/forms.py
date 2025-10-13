# src/companies/forms.py
from django import forms

class CompanyForm(forms.Form):
    name = forms.CharField(
        label="Nom de l'entreprise",
        max_length=100,
        required=True  # Django vérifiera que ce n'est pas vide
    )
    owner = forms.CharField(
        label="Propriétaire (email)",
        required=False # Ce champ est optionnel
    )