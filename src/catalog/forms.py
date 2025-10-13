# src/catalog/forms.py
from django import forms
from companies.service import list_companies

class ProductForm(forms.Form):
    name = forms.CharField(label="Nom du produit", max_length=100)
    sku = forms.CharField(label="SKU (code produit)", max_length=50)
    company_id = forms.ChoiceField(label="Entreprise")
    threshold = forms.IntegerField(label="Seuil d'alerte", required=False)
    # Ajoutez d'autres champs si nécessaire (description, prix...)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On charge dynamiquement la liste des entreprises pour le champ 'company_id'
        companies = list_companies()
        self.fields['company_id'].choices = [(c.id, c.name) for c in companies]