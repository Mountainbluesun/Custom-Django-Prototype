# src/companies/forms.py
from django import forms

class CompanyForm(forms.Form):
    name = forms.CharField(
        label="Company name",
        max_length=100,
        required=True  # Django will verify that it's not empty
    )
    owner = forms.CharField(
        label="Owner (email)",
        required=False # This field is optional
    )