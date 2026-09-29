# File: src/users/forms.py
from django import forms
from companies.models import Company


class UserCreationForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    email = forms.EmailField(label="Email address", required=False)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirm password", widget=forms.PasswordInput)
    is_admin = forms.BooleanField(label="Administrator", required=False)
    companies = forms.ModelMultipleChoiceField(
        label="Companies",
        queryset=Company.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

class UserEditForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    email = forms.EmailField(label="Email address", required=False)
    is_admin = forms.BooleanField(label="Administrator", required=False)
    companies = forms.ModelMultipleChoiceField(
        label="Companies",
        queryset=Company.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Your email address")

class PasswordResetConfirmForm(forms.Form):
    new_password = forms.CharField(label="New password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm new password", widget=forms.PasswordInput)


    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("new_password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data