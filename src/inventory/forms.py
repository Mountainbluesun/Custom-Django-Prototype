from django import forms
from companies.service import list_companies
from catalog.service import list_products
from users.service import list_users

class StockInForm(forms.Form):
    product_id = forms.ChoiceField(label="Produit")
    company_id = forms.ChoiceField(label="Entreprise")
    quantity = forms.IntegerField(label="Quantité", min_value=1)
    note = forms.CharField(label="Note (optionnel)", required=False, widget=forms.Textarea)
    user_id = forms.ChoiceField(label="Utilisateur (Mouvement enregistré par)", required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        allowed_company_ids = user.get("companies", []) if user and not user.get("is_admin") else [c.id for c in list_companies()]

        products = [p for p in list_products() if p.company_id in allowed_company_ids]
        companies = [c for c in list_companies() if c.id in allowed_company_ids]

        self.fields['product_id'].choices = [('', '--- choisir ---')] + [(p.id, p.name) for p in products]
        self.fields['company_id'].choices = [('', '--- choisir ---')] + [(c.id, c.name) for c in companies]
        self.fields['user_id'].choices = [('', '--- choisir ---')] + [(u.id, u.username) for u in list_users()]

class StockOutForm(forms.Form):
    product_id = forms.ChoiceField(label="Produit")
    company_id = forms.ChoiceField(label="Entreprise de sortie")
    quantity = forms.IntegerField(label="Quantité", min_value=1)
    note = forms.CharField(label="Note (optionnel)", required=False, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        allowed_company_ids = user.get("companies", []) if user and not user.get("is_admin") else [c.id for c in list_companies()]
        products = [p for p in list_products() if p.company_id in allowed_company_ids]
        companies = [c for c in list_companies() if c.id in allowed_company_ids]
        self.fields['product_id'].choices = [('', '--- choisir ---')] + [(p.id, p.name) for p in products]
        self.fields['company_id'].choices = [('', '--- choisir ---')] + [(c.id, c.name) for c in companies]



class StockTransferForm(forms.Form):
    product_id = forms.ChoiceField(label="Produit")
    quantity = forms.IntegerField(label="Quantité", min_value=1)
    company_from_id = forms.ChoiceField(label="Depuis l'entreprise")
    company_to_id = forms.ChoiceField(label="Vers l'entreprise")
    note = forms.CharField(label="Note (optionnel)", required=False, widget=forms.Textarea)


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        allowed_company_ids = user.get("companies", []) if user and not user.get("is_admin") else [c.id for c in list_companies()]
        products = [p for p in list_products() if p.company_id in allowed_company_ids]
        companies = [c for c in list_companies() if c.id in allowed_company_ids]

        # 🔎 DEBUG ICI
        print("DEBUG allowed_company_ids:", allowed_company_ids)
        print("DEBUG products:", products)
        print("DEBUG companies:", companies)

        self.fields['product_id'].choices = [('', '--- choisir ---')] + [(p.id, p.name) for p in products]
        self.fields['company_from_id'].choices = [('', '--- choisir ---')] + [(c.id, c.name) for c in companies]
        self.fields['company_to_id'].choices = [('', '--- choisir ---')] + [(c.id, c.name) for c in companies]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('company_from_id') == cleaned_data.get('company_to_id'):
            raise forms.ValidationError("L'entreprise de départ et d'arrivée doivent être différentes.")
        return cleaned_data