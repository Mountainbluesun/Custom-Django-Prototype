import logging
from django import forms
from companies.service import list_companies
from catalog.service import list_products
from users.service import list_users

logger = logging.getLogger(__name__)

class StockInForm(forms.Form):
    product_id = forms.ChoiceField(label="Product")
    company_id = forms.ChoiceField(label="Company")
    quantity = forms.IntegerField(label="Quantity", min_value=1)
    note = forms.CharField(label="Note (optional)", required=False, widget=forms.Textarea)
    user_id = forms.ChoiceField(label="User (Movement recorded by)", required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        allowed_company_ids = user.get("companies", []) if user and not user.get("is_admin") else [c.id for c in list_companies()]

        products = [p for p in list_products() if p.company_id in allowed_company_ids]
        companies = [c for c in list_companies() if c.id in allowed_company_ids]

        self.fields['product_id'].choices = [('', '--- select ---')] + [(p.id, p.name) for p in products]
        self.fields['company_id'].choices = [('', '--- select ---')] + [(c.id, c.name) for c in companies]
        if user and not user.get("is_admin"):
            # Non-admins can only record a movement as themselves
            self.fields['user_id'].choices = [('', '--- select ---'), (user["id"], user["username"])]
        else:
            self.fields['user_id'].choices = [('', '--- select ---')] + [(u.id, u.username) for u in list_users()]
        if user:
            self.fields['user_id'].initial = user.get("id")

class StockOutForm(forms.Form):
    product_id = forms.ChoiceField(label="Product")
    company_id = forms.ChoiceField(label="Outgoing Company")
    quantity = forms.IntegerField(label="Quantity", min_value=1)
    note = forms.CharField(label="Note (optional)", required=False, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        allowed_company_ids = user.get("companies", []) if user and not user.get("is_admin") else [c.id for c in list_companies()]
        products = [p for p in list_products() if p.company_id in allowed_company_ids]
        companies = [c for c in list_companies() if c.id in allowed_company_ids]
        self.fields['product_id'].choices = [('', '--- select ---')] + [(p.id, p.name) for p in products]
        self.fields['company_id'].choices = [('', '--- select ---')] + [(c.id, c.name) for c in companies]



class StockTransferForm(forms.Form):
    product_id = forms.ChoiceField(label="Product")
    quantity = forms.IntegerField(label="Quantity", min_value=1)
    company_from_id = forms.ChoiceField(label="From Company")
    company_to_id = forms.ChoiceField(label="To Company")
    note = forms.CharField(label="Note (optional)", required=False, widget=forms.Textarea)


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        allowed_company_ids = user.get("companies", []) if user and not user.get("is_admin") else [c.id for c in list_companies()]
        products = [p for p in list_products() if p.company_id in allowed_company_ids]
        companies = [c for c in list_companies() if c.id in allowed_company_ids]

        logger.debug("allowed_company_ids=%s, products=%s, companies=%s", allowed_company_ids, products, companies)

        self.fields['product_id'].choices = [('', '--- select ---')] + [(p.id, p.name) for p in products]
        self.fields['company_from_id'].choices = [('', '--- select ---')] + [(c.id, c.name) for c in companies]
        self.fields['company_to_id'].choices = [('', '--- select ---')] + [(c.id, c.name) for c in companies]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('company_from_id') == cleaned_data.get('company_to_id'):
            raise forms.ValidationError("The origin and destination companies must be different.")
        return cleaned_data