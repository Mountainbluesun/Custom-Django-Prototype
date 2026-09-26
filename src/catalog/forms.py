# src/catalog/forms.py
from django import forms
from companies.service import list_companies

class ProductForm(forms.Form):
    name = forms.CharField(label="Product name", max_length=100)
    sku = forms.CharField(label="SKU (product code)", max_length=50)
    company_id = forms.ChoiceField(label="Company")
    threshold = forms.IntegerField(label="Alert threshold", required=False)
    # Add other fields if needed (description, price...)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically load the list of companies for the 'company_id' field
        companies = list_companies()
        self.fields['company_id'].choices = [(c.id, c.name) for c in companies]